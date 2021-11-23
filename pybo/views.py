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

#질문 목록 화면 추가하기
def detail(request, question_id):
    """
        pybo 내용 출력
    """
    question = Question.objects.get(id=question_id)
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context)