import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q, CheckConstraint
from django.utils import timezone


def current_year():
    return datetime.date.today().year


class Hospital(models.Model):
    """
    Hospital Entity Model.
    Represents a hospital facility within the BP Hospitals network.
    
    AT LEAST FOUR DISTINCT CONSTRAINTS / VALIDATIONS ENFORCED:
    1. unique=True on hospital_name: Guarantees no two hospitals can share the same name.
    2. MinValueValidator(1800) & MaxValueValidator(current_year()): Restricts founded_year to realistic values.
    3. max_length limits on all CharFields: Enforces strict length limits (hospital_name <= 200, location <= 255).
    4. blank=False / null=False on required fields: Ensures database and form level mandatory data entry.
    5. Meta CheckConstraint ('check_founded_year_valid'): Database-level constraint ensuring 1800 <= founded_year <= current_year.
    """

    hospital_id = models.BigAutoField(primary_key=True)
    hospital_name = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Hospital Name",
        help_text="Unique name of the hospital facility."
    )
    location = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Location",
        help_text="City/Region location of the hospital."
    )
    founded_year = models.IntegerField(
        null=False,
        blank=False,
        validators=[
            MinValueValidator(1800, message="Founded year cannot be before 1800."),
            MaxValueValidator(current_year(), message="Founded year cannot be in the future.")
        ],
        verbose_name="Founded Year",
        help_text="Year the hospital was established (between 1800 and present)."
    )

    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Hospital"
        verbose_name_plural = "Hospitals"
        ordering = ['-updated_at', 'hospital_name']
        constraints = [
            CheckConstraint(
                condition=Q(founded_year__gte=1800) & Q(founded_year__lte=datetime.date.today().year),
                name="check_founded_year_valid"
            )
        ]

    def __str__(self):
        return f"{self.hospital_name} ({self.location})"
