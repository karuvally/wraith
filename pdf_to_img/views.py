import string
import random
import os
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
        # Save uploaded file with temporary name
        fname = f"{''.join(random.choices(string.ascii_letters, k=10))}.pdf"
        with open(os.path.join("pdf_to_img", fname), "wb") as tmp_file:
            for chunk in request.FILES["pdf_file"].chunks():
                tmp_file.write(chunk)
        request.session["pdf_file"] = fname
        return render(request, "configuration.html", {})
