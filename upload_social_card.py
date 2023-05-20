import io
import os
import pathlib
import textwrap

from PIL import Image, ImageDraw, ImageFont

from azure.storage.blob import BlobServiceClient, ContentSettings


account_url = os.getenv("AZURE_STORAGE_ACCOUNT_URL")
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connection_string)


def check_for_image(
    *,
    check_tag: str,
    tags: dict,
    slug: str,
    extension: str,
):
    """Checks if a blob exists in an Azure Container"""""
    file_blobs = blob_service_client.find_blobs_by_tags(
        filter_expression=f'"{check_tag}" = \'{tags[check_tag]}\''
    )
    filename = pathlib.Path(slug).with_suffix(extension).name
    return filename.name in [f.name for f in file_blobs]

def upload_blob_stream(
    *,
    image: Image,
    extension: str,
    container: str,
    tags: dict,
    slug:str,
):
    """Uploads a blob from a stream to an Azure Container"""""
    if extension.strip(".") in ["jpg", "jpeg"]:
        content_type = "image/jpg"
    elif extension.strip(".") == "png":
        content_type = "image/png"
    else:
        content_type = "application/octet-stream"

    container = container
    tags = {"used_for": "social_cards"}
    filename = pathlib.Path(slug).with_suffix(extension)

    blob_client = blob_service_client.get_blob_client(
        container=container,
        blob=filename,
    )

    # Create a stream to hold the image data
    in_mem_file = io.BytesIO()
    image.save(in_mem_file, format=image.format)
    in_mem_file.seek(0)

    # Upload the image
    blob_client.upload_blob(
        data=in_mem_file,
        blob_type="BlockBlob",
        tags=tags,
        content_settings=ContentSettings(content_type=content_type),
    )


def overlay_text(
    text: str,
    *,
    image_path: str,
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

    font_style = "static/fonts/mononoki Bold Nerd Font Complete.ttf"

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
    font = ImageFont.truetype(font_style, font_size)

    while font.getbbox(text)[1] < image_size_ratio:
        font_size += 1
        font = ImageFont.truetype(font_style, font_size)

    ImageFont.truetype(font_style, 30)
    draw.text((75, 200), text, font=font, fill=(50, 50, 50, 255))
    draw.text(
        (390, 490),
        "kjaymiller.com",
        font = ImageFont.truetype(font_style, 38),
        fill=(50, 50, 50, 255)
        )

    return image