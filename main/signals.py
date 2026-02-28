from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from easy_thumbnails.files import get_thumbnailer
from .models import SliderImage

@receiver(post_delete, sender=SliderImage)
@receiver(post_save, sender=SliderImage)
def clear_thumbnail_cache(sender, instance, **kwargs):
    """Очистка кэша миниатюр при изменении изображения"""
    if instance.image:
        try:
            thumbnailer = get_thumbnailer(instance.image)
            thumbnailer.get_thumbnail({'size': (200, 120)}).delete()
            thumbnailer.get_thumbnail({'size': (100, 60)}).delete()
        except Exception:
            pass