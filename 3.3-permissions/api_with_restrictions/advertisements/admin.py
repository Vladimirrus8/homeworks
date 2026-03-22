from django.contrib import admin
from .models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'creator', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('creator', 'favorites')