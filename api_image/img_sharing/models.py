from django.utils import timezone

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from PIL import Image as PilImage


class StartEndDateMixin(models.Model):
    start_date = models.DateTimeField("Start date", default=timezone.now)
    end_date = models.DateTimeField("End date", blank=True, null=True)

    class Meta:
        abstract = True
        default_manager_name = "objects"

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": ["The deactivation date must not be less than the entry date"]})


class Image(StartEndDateMixin):
    image = models.ImageField(upload_to='images/')
    title = models.TextField(verbose_name="Title", max_length=250)
    image_size = models.IntegerField(verbose_name="Image size", blank=True, null=True)
    expiration_seconds = models.IntegerField(
        verbose_name="Link validity time",
        default=300,
        validators=[MinValueValidator(300), MaxValueValidator(30000)]
    )

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image_size in SubscriptionPlan.objects.values_list('image_size', flat=True):
            img_pillow = PilImage.open(self.image)
            width, height = img_pillow.size
            aspect_ratio = width / height
            new_width = int(self.image_size * aspect_ratio)
            modified_img = img_pillow.resize((new_width, self.image_size))
            modified_img.save(self.image.path)


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    image_size = models.IntegerField(default=200)
    default_link = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Account tier"
        verbose_name_plural = "Account tiers"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}: plan-{self.subscription_plan.name}"
