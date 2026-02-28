from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from adminsortable2.admin import SortableAdminMixin
from .models import SliderImage

@admin.register(SliderImage)
class SliderImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['order', 'admin_thumbnail', 'title', 'is_active', 'created_at']
    list_display_links = ['admin_thumbnail', 'title']
    list_editable = ['is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'alt_text']
    readonly_fields = ['image_preview', 'created_at']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'alt_text')
        }),
        ('Статус', {
            'fields': ('is_active',),
        }),
        ('Превью', {
            'fields': ('image_preview',),
            'classes': ('wide',)
        }),
    )

    def admin_thumbnail(self, obj):
        """Безопасное отображение миниатюры в списке"""
        if obj.image and obj.image.file:
            try:
                return format_html(
                    '<img src="{}" style="max-height: 50px; max-width: 80px; border-radius: 4px;" />',
                    obj.admin_thumbnail_url
                )
            except Exception:
                return format_html('<span style="color: red;">Ошибка загрузки</span>')
        return '-'
    admin_thumbnail.short_description = 'Превью'

    def image_preview(self, obj):
        """Превью на странице редактирования"""
        if obj.image and obj.image.file:
            return format_html(
                '<div style="background: #f0f0f0; padding: 10px; border-radius: 8px;">'
                '<img src="{}" style="max-height: 200px; max-width: 100%; border-radius: 4px;" />'
                '<p style="margin-top: 10px; color: #666;">Путь: {}</p>'
                '</div>',
                obj.image.url,
                obj.image.file.name
            )
        return 'Изображение не загружено'
    image_preview.short_description = 'Предпросмотр'