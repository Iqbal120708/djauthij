import warnings

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def soft_delete(self):
        self.is_active = False
        self.save(update_fields=["is_active"])
    
    def hard_delete(self):
        return super().delete()
    
    def delete(self, *args, **kwargs):
        raise RuntimeError("Gunakan soft_delete() atau hard_delete()")

class OTPVerifications(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField()
    expired_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def clean(self):
        if self.otp and not self.otp.isdigit():
            raise ValidationError({
                'otp': _('Kode OTP harus berupa angka.')
            })
        
        if self.created_at and self.expired_at:
            if self.created_at > self.expired_at:
                raise ValidationError(
                    _('Waktu kedaluwarsa tidak boleh lebih awal dari waktu pembuatan.')
                )
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.user.email} - {self.otp} - {self.is_used}"