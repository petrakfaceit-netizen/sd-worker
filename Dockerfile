FROM timpietruskyblibla/runpod-worker-a1111:3.0.0-base

# Download models
RUN wget -q -O /stable-diffusion-webui/models/Stable-diffusion/majicmixRealistic_v7.safetensors \
    "https://civitai.com/api/download/models/176425" && \
    wget -q -O /stable-diffusion-webui/models/Stable-diffusion/photon_v1.safetensors \
    "https://civitai.com/api/download/models/90072" && \
    wget -q -O /stable-diffusion-webui/models/Stable-diffusion/dreamshaper.safetensors \
    "https://civitai.com/api/download/models/128713"
