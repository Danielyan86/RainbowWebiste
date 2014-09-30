# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render_to_response

def show_rings(request):
    
    return render_to_response('show_rings.html', {'SITE_NAME': "www.yuxin.com",'ring_active':"active"})