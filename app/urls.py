from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('', views.index),
    path('api/v1/status', views.StatusView.as_view()),
    path('api/v1/verify-pincode', views.VerifyPincodeView.as_view()),
    path('api/v1/predict-image', views.PredictImageView.as_view()),
]
