from django.contrib import admin
from .models import HospitalDirector


@admin.register(HospitalDirector)
class HospitalDirectorAdmin(admin.ModelAdmin):
    """
    Django Admin customization for HospitalDirector model.
    """
    list_display = ('director_id', 'director_name', 'qualification', 'hospital')
    search_fields = ('director_name', 'qualification', 'hospital__hospital_name')
    list_filter = ('hospital',)
    ordering = ('director_id',)
