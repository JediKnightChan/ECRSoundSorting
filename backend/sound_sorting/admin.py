from django.contrib import admin

from .models import GameFolder, SoundItem, SoundCategory, SoundItemReview

# Register your models here.
admin.site.register(GameFolder)
admin.site.register(SoundItem)
admin.site.register(SoundCategory)
admin.site.register(SoundItemReview)
