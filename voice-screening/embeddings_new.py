import torch
import numpy as np
import os
from transformers import Wav2Vec2Processor, Wav2Vec2Model
from preprocess import preprocess_audio

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
wav2vec   = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base-960h")

CHUNK_SECONDS = 30
SAMPLE_RATE   = 16000
CHUNK_SIZE    = CHUNK_SECONDS * SAMPLE_RATE

def get_embedding_chunked(waveform):
    chunks = waveform.split(CHUNK_SIZE)
    chunk_embeddings = []
    for chunk in chunks:
        if len(chunk) < SAMPLE_RATE:
            continue
        inputs = processor(
            chunk.numpy(),
            sampling_rate=SAMPLE_RATE,
            return_tensors="pt",
            padding=True
        )
        with torch.no_grad():
            outputs = wav2vec(**inputs)
        emb = outputs.last_hidden_state.mean(dim=1)
        chunk_embeddings.append(emb)
    return torch.stack(chunk_embeddings).mean(dim=0)

if __name__ == "__main__":
    audio_dir  = "/Users/shreya/voice-health/data/raw"
    daic_root  = "/Users/shreya/voice-health/DAIC-WOZ"

    # Load what we already have
    old_emb = np.load("/Users/shreya/voice-health/features/embeddings.npy").squeeze()
    old_ids = np.load("/Users/shreya/voice-health/features/processed_ids.npy")
    print(f"Already have {len(old_ids)} embeddings")

    # Find new audio files not yet processed
    all_audio = [f for f in os.listdir(audio_dir) if f.endswith(".wav")]
    new_files = [f for f in all_audio if int(f.replace(".wav","")) not in old_ids]
    print(f"New files to process: {len(new_files)}")

    new_embeddings = []
    new_ids        = []

    for i, fname in enumerate(sorted(new_files)):
        pid  = int(fname.replace(".wav", ""))
        path = os.path.join(audio_dir, fname)
        print(f"[{i+1}/{len(new_files)}] Processing {pid}...")
        try:
            waveform = preprocess_audio(path)
            emb      = get_embedding_chunked(waveform)
            new_embeddings.append(emb.numpy())
            new_ids.append(pid)
            if len(new_embeddings) % 5 == 0:
                print(f"  Checkpoint: {len(new_embeddings)} new done so far")
        except Exception as e:
            print(f"  ERROR on {pid}: {e}, skipping")

    # Merge old + new
    all_emb = np.vstack([old_emb, np.array(new_embeddings).squeeze()])
    all_ids = np.concatenate([old_ids, np.array(new_ids)])

    np.save("/Users/shreya/voice-health/features/embeddings.npy", all_emb)
    np.save("/Users/shreya/voice-health/features/processed_ids.npy", all_ids)
    print(f"\nDone — total embeddings saved: {len(all_ids)}")
