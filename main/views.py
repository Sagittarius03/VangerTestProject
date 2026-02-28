from django.shortcuts import render
from .models import SliderImage


def home(request):
    return render(request, 'base.html', context={
        'title': "Космическое агентство",
        'slider_images': SliderImage.objects.filter(
            is_active=True
        ).select_related('image')
    })