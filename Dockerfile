FROM ashleykleynhans/stable-diffusion-webui:2.5.1

# Download models
RUN mkdir -p /stable-diffusion-webui/models/Stable-diffusion && \
    wget -q -O /stable-diffusion-webui/models/Stable-diffusion/majicmixRealistic_v7.safetensors \
    "https://civitai.com/api/download/models/176425" && \
    wget -q -O /stable-diffusion-webui/models/Stable-diffusion/photon_v1.safetensors \
    "https://civitai.com/api/download/models/90072" && \
    wget -q -O /stable-diffusion-webui/models/Stable-diffusion/dreamshaper.safetensors \
    "https://civitai.com/api/download/models/128713"

COPY src/handler.py /handler.py
COPY src/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
