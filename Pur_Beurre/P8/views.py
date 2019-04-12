from django.shortcuts import render
from django.http import HttpResponse

def Legal_notice(request):
    return render(request, 'Legal_Notice.html')

# Create your views here.
