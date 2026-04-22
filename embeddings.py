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
    audio_dir = "/Users/shreya/voice-health/data/raw"
    ids       = np.load("/Users/shreya/voice-health/features/participant_ids.npy")
    save_path = "/Users/shreya/voice-health/features/embeddings.npy"
    done_path = "/Users/shreya/voice-health/features/processed_ids.npy"

    embeddings = []
    done_ids   = []

    for i, pid in enumerate(ids):
        path = os.path.join(audio_dir, f"{pid}.wav")
        if not os.path.exists(path):
            print(f"Missing: {pid}, skipping")
            continue
        print(f"[{i+1}/{len(ids)}] Processing {pid}...")
        try:
            waveform = preprocess_audio(path)
            emb      = get_embedding_chunked(waveform)
            embeddings.append(emb.numpy())
            done_ids.append(pid)
            if len(embeddings) % 5 == 0:
                np.save(save_path, np.array(embeddings))
                np.save(done_path, np.array(done_ids))
                print(f"  Checkpoint saved ({len(embeddings)} done)")
        except Exception as e:
            print(f"  ERROR on {pid}: {e}, skipping")

    np.save(save_path, np.array(embeddings))
    np.save(done_path, np.array(done_ids))
    print(f"\nDone — saved {len(embeddings)} embeddings")
