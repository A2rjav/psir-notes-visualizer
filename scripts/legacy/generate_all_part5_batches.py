import os
import sys

def create_batches():
    output_dir = "transcriptions_paper1_part5"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating 15 batch files in {output_dir}...")

if __name__ == "__main__":
    create_batches()
