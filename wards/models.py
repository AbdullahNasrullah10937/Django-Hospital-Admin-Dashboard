from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q, CheckConstraint
from django.utils import timezone
from hospitals.models import Hospital


class Ward(models.Model):
    """
    Ward Entity Model.
    Represents a specific department/ward within a hospital facility (e.g., Cardiology, ICU, Pediatrics).
    
    AT LEAST FOUR DISTINCT CONSTRAINTS / VALIDATIONS ENFORCED:
    1. ForeignKey with null=False: Every ward must be assigned to an existing Hospital facility.
    2. MinValueValidator(1) on capacity: Ensures a ward has at least 1 bed capacity.
    3. MaxValueValidator(500) on capacity: Prevents unrealistic ward bed allocations (max 500 beds).
    4. max_length limit on ward_name: Enforces length boundary (ward_name <= 150 chars).
    5. Meta CheckConstraint ('check_ward_capacity_valid'): DB-level CheckConstraint ensuring 0 < capacity <= 500.
    """

    ward_id = models.BigAutoField(primary_key=True)
    ward_name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        verbose_name="Ward Name",
        help_text="Name of the ward (e.g., Cardiac ICU, Pediatrics Wing A)."
    )
    capacity = models.IntegerField(
        null=False,
        blank=False,
        validators=[
            MinValueValidator(1, message="Ward capacity must be at least 1 bed."),
            MaxValueValidator(500, message="Ward capacity cannot exceed 500 beds.")
        ],
        verbose_name="Capacity (Beds)",
        help_text="Maximum number of beds in this ward (1-500)."
    )

    # Relationship: One Hospital has Many Wards
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name='wards',
        null=False,
        blank=False,
        verbose_name="Hospital",
        help_text="The hospital facility this ward belongs to."
    )

    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Ward"
        verbose_name_plural = "Wards"
        ordering = ['-updated_at', 'ward_name']
        constraints = [
            CheckConstraint(
                condition=Q(capacity__gt=0) & Q(capacity__lte=500),
                name="check_ward_capacity_valid"
            )
        ]

    def __str__(self):
        return f"{self.ward_name} ({self.hospital.hospital_name}) - {self.capacity} Beds"
