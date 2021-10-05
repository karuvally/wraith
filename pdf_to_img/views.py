from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# Create your views here.
class UploadPDF(View):
    def get(self, request):
        return render(request, "upload_pdf.html", {})

    def post(self, request):
        if not request.FILES:
            return HttpResponse("Not a valid file...")
        request.session["pdf_upload"] = request.FILES["pdf_file"]
        return render(request, "configuration.html", {})
