from django.urls import path
from v1.views import get_qr


urlpatterns = [
    path('v1/', get_qr)
]
