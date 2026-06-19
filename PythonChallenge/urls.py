from django.contrib import admin
from django.urls import path

from python_challenge.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path("indices", GetValuesView.as_view(), name="indices_ipc"),
]

