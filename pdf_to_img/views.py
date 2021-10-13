import string
import random
import os
import shutil
import pathlib
import mimetypes

from django.shortcuts import render, resolve_url, redirect
from django.views import View
from django.http import HttpResponse

from pdf2image import convert_from_path
from pdf2image.exceptions import(
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

import pdb # debug

# TODO
# Verify if uploaded file is PDF
# Delete tmp dirs not part of any sessions
# Use UUID instead of random tmp dir name
# Enable handing of exceptions
# Redirect user to homepage after returning converted files

class UploadPDF(View):
    def get(self, request):
        return render(request, "upload_pdf.html", {})

    def post(self, request):
        """Deal with uploaded PDF file"""
        if not request.FILES:
            return HttpResponse("Not a valid file...")

        # Create directory for storing temporary files
        if not os.path.isdir(os.path.join("pdf_to_img", "tmp")):
            os.mkdir(os.path.join("pdf_to_img", "tmp"))
        tmp_dir = os.path.join(
            "pdf_to_img", "tmp",
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
        return redirect(resolve_url("pdf_to_img:convert_pdf"))

class ConvertPDF(View):
    def get(self, request):
        return render(request, "convert.html", {})
    
    def post(self, request):
        # Convert PDF
        format = request.POST["format"]
        pdf_name = request.session["pdf_name"]
        tmp_dir = request.session["tmp_dir"]
        convert_from_path(
            pdf_path=os.path.join(tmp_dir, "upload.pdf"),
            output_file=pdf_name[:pdf_name.index(".pdf")],
            output_folder=tmp_dir,
            fmt=format,
        )
        
        # Archive the converted files
        os.remove(os.path.join(tmp_dir, "upload.pdf"))
        shutil.make_archive(
            base_name=tmp_dir,
            format="zip",
            root_dir=pathlib.Path(tmp_dir).parent,
            base_dir=os.path.basename(tmp_dir)
        )
        shutil.rmtree(tmp_dir)
        
        # Return the archive to user
        return HttpResponse(
            open(f"{tmp_dir}.zip", "rb"),
            content_type=mimetypes.guess_type(f"{tmp_dir}.zip"),
            headers={
                "Content-Disposition": f"attachment; filename={pdf_name}.zip"
            }
        )
