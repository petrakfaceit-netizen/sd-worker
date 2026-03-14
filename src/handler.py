import runpod
import subprocess
import requests
import time
import base64
import os

WEBUI_URL = "http://127.0.0.1:7860"

def wait_for_webui():
    for i in range(180):
        try:
            r = requests.get(f"{WEBUI_URL}/sdapi/v1/sd-models", timeout=3)
            if r.status_code == 200:
                print("A1111 ready!")
                return True
        except:
            pass
        time.sleep(2)
    return False

# Start A1111
proc = subprocess.Popen([
    "python", "/stable-diffusion-webui/webui.py",
    "--nowebui", "--api", "--xformers",
    "--no-half-vae", "--skip-torch-cuda-test"
], cwd="/stable-diffusion-webui")

print("Waiting for A1111...")
wait_for_webui()

def handler(job):
    inp = job.get("input", {})
    
    payload = {
        "prompt": inp.get("prompt", ""),
        "negative_prompt": inp.get("negative_prompt", ""),
        "steps": inp.get("steps", 20),
        "cfg_scale": inp.get("cfg_scale", 7),
        "width": inp.get("width", 512),
        "height": inp.get("height", 512),
        "sampler_name": inp.get("sampler_name", "Euler"),
        "seed": inp.get("seed", -1),
    }
    
    init_images = inp.get("init_images")
    if init_images:
        payload["init_images"] = init_images
        payload["denoising_strength"] = inp.get("denoising_strength", 0.75)
        url = f"{WEBUI_URL}/sdapi/v1/img2img"
    else:
        url = f"{WEBUI_URL}/sdapi/v1/txt2img"
    
    r = requests.post(url, json=payload, timeout=300)
    result = r.json()
    
    return {"images": result.get("images", [])}

runpod.serverless.start({"handler": handler})
