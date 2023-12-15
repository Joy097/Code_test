from django.shortcuts import render
from django.http import HttpResponse


def show_page(request): 
    return render(request,'home.html')