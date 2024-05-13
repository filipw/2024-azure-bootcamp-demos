from promptflow.contracts.multimedia import Image as PFImage

def is_valid(image: PFImage):
    return image._mime_type != "image/*"