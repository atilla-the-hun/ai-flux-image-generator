import replicate
import time
from PIL import Image
import requests
from io import BytesIO

def generate_image(prompt, num_outputs, aspect_ratio, output_format, output_quality=100):
    # Start the image generation process
    start_time = time.time()
    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input={
            "prompt": prompt,
            "num_outputs": num_outputs,
            "aspect_ratio": aspect_ratio,
            "output_format": output_format,
            "output_quality": output_quality,
        }
    )

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Convert output URLs to PIL Images
    generated_images = []
    for img_url in output:
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        generated_images.append(img)

    return generated_images, elapsed_time
