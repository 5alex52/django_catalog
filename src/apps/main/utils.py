from uuid import uuid4

from PIL import Image
from PIL import ImageOps
from pytils.translit import slugify


def unique_slugify(instance, slug):
    """
    Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
    """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{unique_slug}-{uuid4().hex[:8]}"
    return unique_slug


def image_compress(image_path, height, width):
    """
    Оптимизация изображений
    """
    img = Image.open(image_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    if img.height > height or img.width > width:
        output_size = (height, width)
        img.thumbnail(output_size)
    img = ImageOps.exif_transpose(img)
    img.save(image_path, format="JPEG", quality=100, optimize=True)


def collection_directory_path(instance, filename):
    return "collection_{0}/{1}".format(instance.slug, filename)


def image_directory_path(instance, filename):
    return "category_{0}/product_{1}/{2}".format(
        instance.product.category.slug, instance.product.slug, filename
    )


def product_directory_path(instance, filename):
    return "category_{0}/product_{1}/{2}".format(
        instance.category.slug, instance.slug, filename
    )
