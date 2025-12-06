import requests
from io import BytesIO
from PIL import Image


def generate_poster_with_stable_diffusion(analysis: dict, seed: int = 42):
    """调用 Stability AI Stable Diffusion（sd3）生成 1:1 艺术海报。"""
    api_key = analysis.get("stability_key")
    if not api_key:
        print("No STABILITY_API_KEY found in analysis / environment.")
        return None

    mood = analysis.get("mood", "calm nostalgic")
    palette = analysis.get("palette", [])
    style_mode = analysis.get("style_mode", "misty_gradient")

    palette_str = ", ".join(palette) if isinstance(palette, (list, tuple)) else str(palette)

    prompt = (
        "abstract emotional poster design, 1:1 aspect ratio, "
        f"mood: {mood}, "
        f"color palette: {palette_str}, "
        f"visual style: {style_mode}, "
        "soft gradients, dreamy atmosphere, subtle grain, "
        "cinematic lighting, minimalist composition, high quality illustration, "
        "no text in the image, focus on abstract shapes and color fields."
    )

    url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

    headers = {
        "authorization": f"Bearer {api_key}",
        "accept": "image/*",
    }

    data = {
        "prompt": prompt,
        "output_format": "png",
        "seed": str(seed),
    }

    try:
        resp = requests.post(
            url,
            headers=headers,
            files={"none": ""},
            data=data,
            timeout=60,
        )

        if resp.status_code != 200:
            print("Stable Diffusion error:", resp.status_code, resp.text)
            return None

        img_bytes = resp.content
        img = Image.open(BytesIO(img_bytes)).convert("RGB")
        return img

    except Exception as e:
        print("Stable Diffusion exception:", e)
        return None
