import argparse
import os
import sys

sys.path.insert(0, '/stable-diffusion-webui')
os.chdir('/stable-diffusion-webui')

# Minimal cache script to preload model
parser = argparse.ArgumentParser()
parser.add_argument('--use-cpu', default='all')
parser.add_argument('--ckpt', required=True)
args = parser.parse_args()

print(f"Cache script initialized for {args.ckpt}")
print("Model will be loaded on first request")
