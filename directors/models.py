from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from hospitals.models import Hospital


class HospitalDirector(models.Model):
    """
    Hospital Director Entity Model.
    Represents the executive director presiding over a specific hospital facility.
    
    AT LEAST FOUR DISTINCT CONSTRAINTS / VALIDATIONS ENFORCED:
    1. OneToOneField with null=False: Enforces mandatory 1-to-1 relationship with Hospital entity.
    2. unique=True (implied by OneToOneField): Guarantees each hospital can have at most ONE director, and vice versa.
    3. max_length limits: Restricts director_name (<= 150 chars) and qualification (<= 200 chars).
    4. clean() validation: Custom model validation verifying director_name is not purely numeric, empty, or whitespace.
    5. on_delete=CASCADE justified: If a hospital is removed, its associated director record is cascade-deleted 
       to preserve referential integrity without orphan records.
    """

    director_id = models.BigAutoField(primary_key=True)
    director_name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        verbose_name="Director Name",
        help_text="Full name of the medical director (e.g., Dr. Sarah Jenkins)."
    )
    qualification = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name="Qualification",
        help_text="Academic/Medical qualifications (e.g., MD, PhD, MHA)."
    )

    # Relationship: One Hospital has One Director
    hospital = models.OneToOneField(
        Hospital,
        on_delete=models.CASCADE,
        related_name='director',
        null=False,
        blank=False,
        verbose_name="Assigned Hospital",
        help_text="The hospital facility assigned to this director."
    )

    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def clean(self):
        """Custom validation for director_name."""
        super().clean()
        if self.director_name:
            stripped_name = self.director_name.strip()
            if not stripped_name:
                raise ValidationError({'director_name': "Director name cannot consist only of whitespace."})
            if stripped_name.isdigit():
                raise ValidationError({'director_name': "Director name cannot be purely numeric."})

    class Meta:
        verbose_name = "Hospital Director"
        verbose_name_plural = "Hospital Directors"
        ordering = ['-updated_at', 'director_name']

    def __str__(self):
        return f"{self.director_name} - {self.qualification} ({self.hospital.hospital_name})"
