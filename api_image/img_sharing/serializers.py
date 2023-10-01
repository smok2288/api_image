from django.utils import timezone
from rest_framework import serializers
from .models import UserProfile, Image, SubscriptionPlan


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    subscription_plan = SubscriptionPlanSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'title', "expiration_seconds")

