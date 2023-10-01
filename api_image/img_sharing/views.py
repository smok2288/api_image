from rest_framework import status, viewsets
from rest_framework.response import Response
from django.utils import timezone
from PIL import Image as PilImage
from datetime import timedelta
from .models import Image, SubscriptionPlan
from .serializers import ImageSerializer


class ImageUploadView(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.userprofile.subscription_plan != 'Premium':
            image_size = SubscriptionPlan.objects.get(name=self.request.user.userprofile.subscription_plan).image_size
            queryset = Image.objects.filter(image_size__lte=image_size, end_date__lte=timezone.now())
        else:
            queryset = super().get_queryset()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer_obj = ImageSerializer(data=request.data)
        title = request.data.get('title', '')

        if serializer_obj.is_valid():
            image_data = request.data.get('image')
            image_height = PilImage.open(image_data).height

            # Create and save the original image
            original_instance = Image(image=image_data, title=title, image_size=image_height)
            original_instance.save()
            serializer = self.get_serializer(original_instance)

            # Create and save images with different heights
            new_heights = SubscriptionPlan.objects.values_list('image_size', flat=True)
            expiration_seconds = int(request.data.get('expiration_seconds', 0))
            for new_height in new_heights:
                instance = Image(
                    image=image_data,
                    title=f"{title}_{new_height}",
                    image_size=new_height,
                    end_date=timezone.now() + timedelta(seconds=expiration_seconds)
                )
                instance.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
