import string
import random
import os
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from pdf2image import convert_from_path
from pdf2image.exceptions import(
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

class UploadPDF(View):
    def get(self, request):
        return render(request, "upload_pdf.html", {})

    # TODO
    # Verify if uploaded file is PDF
    def post(self, request):
        """Deal with uploaded PDF file"""
        if not request.FILES:
            return HttpResponse("Not a valid file...")

        # Create directory for storing temporary files
        if not os.path.isdir(os.path.join("pdf_to_img", "tmp")):
            os.mkdir(os.path.join("pdf_to_img", "tmp"))

        # Save uploaded file with temporary name
        fname = os.path.join(
            "pdf_to_img",
            "tmp",
            f"{''.join(random.choices(string.ascii_letters, k=10))}.pdf"
        )
        with open(fname, "wb") as tmp_file:
            for chunk in request.FILES["pdf_file"].chunks():
                tmp_file.write(chunk)
        request.session["pdf_file"] = fname

        # Redirect user to the next page
        return render(request, "convert.html", {})

class ConvertPDF(View):
    def post(self, request):
        pass
