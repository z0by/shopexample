from models import ProductImage


def get_im_source(p):
    try:
        image_source = ProductImage.objects.get(product=p).url
    except Exception:
        image_source = "/media/images/350_260.png"
    return image_source


def get_im_20(p):
    try:
        image_20 = ProductImage.objects.get(product=p).url20
    except Exception:
        image_20 = "/media/images/350_260.png"
    return image_20

def get_im_30(p):
    try:
        image_30 = ProductImage.objects.get(product=p).url20
    except Exception:
        image_30 = "/media/images/350_260.png"
    return image_30
