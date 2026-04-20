import os
import shutil

daic_root  = "/Users/shreya/voice-health/DAIC-WOZ"
output_dir = "/Users/shreya/voice-health/data/raw"

copied = 0
for fname in os.listdir(daic_root):
    if fname.endswith("_AUDIO.wav"):
        pid = fname.replace("_AUDIO.wav", "")
        dst = os.path.join(output_dir, f"{pid}.wav")
        if not os.path.exists(dst):  # only copy new ones
            src = os.path.join(daic_root, fname)
            shutil.copy(src, dst)
            print(f"Copied {pid}")
            copied += 1

print(f"\nCopied {copied} new audio files")
