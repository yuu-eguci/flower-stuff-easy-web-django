"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from app import views
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings


app_name = 'app'
urlpatterns = [
    path('', views.index),
    path('api/v1/boot', views.BootView.as_view()),
    path('api/v1/verify-pincode', views.Verify_pincode.as_view()),
    path('api/v1/predict-image', views.Predict_image.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
