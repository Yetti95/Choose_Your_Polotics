from django.shortcuts import render
from django.http import HttpResponse

def aboutUs (request) :
    return HttpResponse ("<h2> About the Four Fathers </h2>")
# Create your views here.
