from django.db import models
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField
from easy_thumbnails.files import get_thumbnailer
from django.core.cache import cache

class SliderImage(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name=_('Название')
    )
    
    image = FilerImageField(
        on_delete=models.CASCADE,
        verbose_name=_('Изображение'),
        related_name='slider_images',
        null=True,
        blank=False
    ) 
    
    alt_text = models.CharField(
        max_length=255,
        verbose_name=_('Alt текст'),
        blank=True
    )
    
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Порядок'),
        db_index=True
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Активно')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )

    class Meta:
        verbose_name = _('Изображение слайдера')
        verbose_name_plural = _('Изображения слайдера')
        ordering = ['order']

    def __str__(self):
        return self.title

    @property
    def large_url(self):
        """Безопасное получение URL большого изображения"""
        if self.image and self.image.file:
            return self.image.url
        return ''

    @property
    def thumbnail_url(self):
        """Используем оригинал для миниатюр"""
        if self.image and self.image.file:
            return self.image.url
        return ''
        

    @property
    def admin_thumbnail_url(self):
        """Миниатюра для админки"""
        if not self.image or not self.image.file:
            return ''
        
        try:
            thumbnailer = get_thumbnailer(self.image)
            thumbnail = thumbnailer.get_thumbnail({
                'size': (100, 60),
                'crop': True,
                'upscale': True,
                'quality': 90
            })
            return thumbnail.url
        except Exception:
            return self.image.url