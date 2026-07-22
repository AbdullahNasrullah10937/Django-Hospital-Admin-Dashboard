from django.contrib import admin
from .models import Hospital


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    """
    Django Admin customization for Hospital model.
    """
    list_display = ('hospital_id', 'hospital_name', 'location', 'founded_year')
    search_fields = ('hospital_name', 'location')
    list_filter = ('founded_year', 'location')
    ordering = ('hospital_id',)
