from django.urls import path

from . import upload_views, views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", upload_views.FileUploadView.as_view(), name="upload"),
]
