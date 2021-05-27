"""buskoin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from api import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', views.BuskoinCustomAuthentication.as_view()),
    path('api/sign-up/', views.create_account),
    path('api/profile/', views.profile),
    path('api/create-payment/', views.create_payment_intent),
    path('api/fetch-profile/<uuid:pk>/', views.fetch_profile),
    path('api/fetch-payment/<uuid:pk>/', views.fetch_payment),
    path('api/create_stripe_login/', views.create_stripe_login),
    path('api/search_profiles/', views.search_profiles),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)