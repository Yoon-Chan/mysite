from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.shortcuts import render

# Create your views here.
def index(request):
    # pybo 목록 출력(Question)
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list' : question_list}

    #render로 화면 출력하기
    return render(request, 'pybo/question_list.html', context)
    #return HttpResponse(context['question_list'])