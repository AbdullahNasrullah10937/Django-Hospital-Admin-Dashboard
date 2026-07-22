from django.contrib import admin
from .models import Ward


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    """
    Django Admin customization for Ward model.
    """
    list_display = ('ward_id', 'ward_name', 'capacity', 'hospital')
    search_fields = ('ward_name', 'hospital__hospital_name')
    list_filter = ('hospital',)
    ordering = ('ward_id',)
