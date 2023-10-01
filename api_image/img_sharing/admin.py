from django.contrib import admin
from .models import UserProfile, Image, SubscriptionPlan

admin.site.register(UserProfile)
admin.site.register(Image)
admin.site.register(SubscriptionPlan)