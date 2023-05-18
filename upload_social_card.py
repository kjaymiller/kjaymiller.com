import pathlib
import textwrap

from PIL import Image, ImageDraw, ImageFont


def overlay_text(
    text: str,
    *,
    image_path: str,
    output_path: str
) -> None:
    """Add text over an image"""

    # Wrap the text
    wrap_cap_2xl = 45
    wrap_cap_xl = 35
    wrap_cap_lg = 10

    wrap_length_xl = 25
    wrap_length_lg =20
    wrap_length_md = 15
    wrap_length_sm = 12

    image = Image.open(image_path)

    if pathlib.Path(image_path).suffix == ".png":
        image = image.convert("RGB")

    font_style = "/mononoki Bold Nerd Font Complete.ttf"

    if (text_length := len(text)) >= wrap_cap_2xl:
        text = textwrap.fill(text, width=wrap_length_xl)
        image_size_ratio = image.size[0] * 0.006
    elif text_length >= wrap_cap_xl:
        image_text_size = "xl"
        text = textwrap.fill(text, width=wrap_length_lg)
        image_size_ratio = image.size[0] * 0.008
    elif text_length >= wrap_cap_lg:
        image_text_size = "lg"
        text = textwrap.fill(text, width=wrap_length_md)
        image_size_ratio = image.size[0] * 0.01
    else:
        image_text_size = "md"
        text = textwrap.fill(text, width=wrap_length_sm)
        image_size_ratio = image.size[0] * 0.012

    draw = ImageDraw.Draw(image)
    font_size = 1
    font = ImageFont.truetype("static/fonts/mononoki Bold Italic Nerd Font Complete.ttf", font_size)

    while font.getbbox(text)[1] < image_size_ratio:
        font_size += 1
        font = ImageFont.truetype(font_style, font_size)

    ImageFont.truetype("Arial", 30)
    draw.text((75, 200), text, font=font, fill=(50, 50, 50, 255))
    draw.text(
        (390, 490),
        "kjaymiller.com",
        font = ImageFont.truetype(font_style, 38),
        fill=(50, 50, 50, 255)
        )
    image.save(output_path)