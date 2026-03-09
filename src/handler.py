import runpod
import subprocess
import os
import time
import base64
import requests

# Start A1111 in background
def start_webui():
    os.chdir('/stable-diffusion-webui')
    subprocess.Popen([
        'python', 'webui.py',
        '--nowebui',
        '--api',
        '--xformers',
        '--no-half-vae'
    ])
    # Wait for API to be ready
    for i in range(120):
        try:
            r = requests.get('http://127.0.0.1:7860/sdapi/v1/sd-models', timeout=5)
            if r.status_code == 200:
                print("A1111 API ready!")
                return True
        except:
            pass
        time.sleep(2)
    return False

# Initialize
start_webui()

def handler(event):
    inp = event.get('input', {})
    
    prompt = inp.get('prompt', 'a cat')
    negative_prompt = inp.get('negative_prompt', '')
    steps = inp.get('steps', 20)
    cfg_scale = inp.get('cfg_scale', 7)
    width = inp.get('width', 512)
    height = inp.get('height', 512)
    sampler_name = inp.get('sampler_name', 'Euler')
    seed = inp.get('seed', -1)
    
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "width": width,
        "height": height,
        "sampler_name": sampler_name,
        "seed": seed
    }
    
    # img2img
    init_images = inp.get('init_images')
    if init_images:
        payload['init_images'] = init_images
        payload['denoising_strength'] = inp.get('denoising_strength', 0.75)
        url = 'http://127.0.0.1:7860/sdapi/v1/img2img'
    else:
        url = 'http://127.0.0.1:7860/sdapi/v1/txt2img'
    
    r = requests.post(url, json=payload)
    result = r.json()
    
    return {"images": result.get('images', [])}

runpod.serverless.start({"handler": handler})
