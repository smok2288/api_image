from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'img_sharing'

router = SimpleRouter()
router.register(r'', views.ImageUploadView, basename='upload')

urlpatterns = [
    path('', include(router.urls)),
]