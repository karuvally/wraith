from django.urls import path, include
from .views import UploadPDF, ConvertPDF

app_name = "pdf_to_img"
urlpatterns = [
    path("upload/", UploadPDF.as_view(), name="upload_pdf"),
    path("convert/", ConvertPDF.as_view(), name="convert_pdf"),
]
