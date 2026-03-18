import runpod
import requests
import time
import subprocess
import os

WEBUI_URL = "http://127.0.0.1:7860"

def wait_for_webui(timeout=300):
    print("Waiting for A1111 WebUI...")
    for i in range(timeout):
        try:
            r = requests.get(f"{WEBUI_URL}/sdapi/v1/sd-models", timeout=2)
            if r.status_code == 200:
                print(f"A1111 ready after {i}s!")
                return True
        except:
            pass
        time.sleep(1)
    print("A1111 failed to start!")
    return False

# Remove root check from webui.sh and start A1111
subprocess.Popen(
    "cd /workspace/stable-diffusion-webui && "
    "sed -i '/cannot be run as root/d' webui.sh && "
    "sed -i '/can.t be run as root/d' webui.sh && "
    "sed -i '/running as root/d' webui.sh && "
    "sed -i '/\\$EUID.*0/d' webui.sh && "
    "bash webui.sh --nowebui --api --xformers --no-half-vae --skip-install",
    shell=True
)

print("Waiting for A1111...")
wait_for_webui()

def handler(job):
    inp = job.get("input", {})
    
    # Switch model if requested
    model = inp.get("model")
    if model:
        requests.post(f"{WEBUI_URL}/sdapi/v1/options", json={"sd_model_checkpoint": model})
        time.sleep(2)
    
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
