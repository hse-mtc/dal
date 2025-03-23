from django.db import models


class MilitaryOffice(models.Model):
    """Model representing a military registration office."""
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    is_custom = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Military Office"
        verbose_name_plural = "Military Offices"
    
    def __str__(self):
        return self.name
