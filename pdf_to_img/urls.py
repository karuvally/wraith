from django.urls import path, include

app_name = "pdf_to_img"
urlpatterns = [
    path('upload/', "upload_pdf.html", name="upload_pdf"),
]
