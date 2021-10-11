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

import pdb

class UploadPDF(View):
    def get(self, request):
        return render(request, "upload_pdf.html", {})

    # TODO
    # Verify if uploaded file is PDF
    # Delete tmp dirs not part of any sessions
    def post(self, request):
        """Deal with uploaded PDF file"""
        if not request.FILES:
            return HttpResponse("Not a valid file...")

        # Create directory for storing temporary files
        if not os.path.isdir(os.path.join("pdf_to_img", "tmp")):
            os.mkdir(os.path.join("pdf_to_img", "tmp"))
        tmp_dir = os.path.join(
            "pdf_to_img",
            "tmp",
            "".join(random.choices(string.ascii_letters, k=10))
        )
        os.mkdir(tmp_dir)
        request.session["tmp_dir"] = tmp_dir
        
        # Save uploaded file inside tmp dir
        with open(os.path.join(tmp_dir, "upload.pdf"), "wb") as pdf_file:
            for chunk in request.FILES["pdf_file"].chunks():
                pdf_file.write(chunk)
        request.session["pdf_name"] = request.FILES["pdf_file"].name

        # Redirect user to the next page
        return render(request, "convert.html", {})

class ConvertPDF(View):
    def post(self, request):
        pass
