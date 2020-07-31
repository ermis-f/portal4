# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return render(request,'index.html')


def about(request):
    return render(request,'about.html')


def help(request):
    return render(request,'help.html')


def contact(request):
    return render(request,'contact.html')


def workshop(request):
    return render(request,'workshop.html')

def cyprus(request):
    return render(request,'maps/cyprus.html')

def crete(request):
    return render(request,'maps/crete.html')

def lesvos(request):
    return render(request,'maps/lesvos.html')




# Create your views here.
