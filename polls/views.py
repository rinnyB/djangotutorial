from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    resp = "Hello World. You are at polls index!"
    return HttpResponse(resp)

def detail(request, question_id):
    resp = "You're looking at question %s." 
    return HttpResponse(resp % question_id)

def results(request, question_id):
    resp = "You're looking at results of question %s"
    return HttpResponse(resp % question_id)

def vote(request, question_id):
    resp = "You're voting on question %s."
    return HttpResponse(resp % question_id)
    