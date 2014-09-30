'''
Created on 2013-10-10

@author: yannpxia
'''
from django.http import HttpResponse

from django.shortcuts import render_to_response

def homepage(request):
    
    return render_to_response('homepage.html', {'SITE_NAME': "www.rainbow1314.com", 'first_active':'active'})