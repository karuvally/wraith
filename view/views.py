from django.shortcuts import render
from django.views import View

# Create your views here.
class Overview(View):
    template_name = "overview.html"
    
    def get(self, request):
        return render(request, template_name, {})    
