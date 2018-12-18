from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404


from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by("-publication_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    resp = "You're looking at question %s." 
    return HttpResponse(resp % question_id)

def results(request, question_id):
    resp = "You're looking at results of question %s"
    return HttpResponse(resp % question_id)

def vote(request, question_id):
    resp = "You're voting on question %s."
    return HttpResponse(resp % question_id)
    