from django.shortcuts import render
from django.http import HttpResponse

def Legal_notice(request):
    return render(request, 'P8/base.html')

# Create your views here.
