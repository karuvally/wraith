from django.shortcuts import render
from django.views import View

# Create your views here.
class UploadPDF(View):
    def get(self, request):
        return render(request, "upload_pdf.html", {})
