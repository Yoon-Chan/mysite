from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import request

from ..models import Question
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..forms import QuestionForm
from django.contrib.auth.decorators import  login_required
from django.contrib import messages

#페이지 기능 구현하기 위한 사용 모듈
from django.core.paginator import  Paginator

@login_required(login_url='common:login')
def question_create(request):
    """
        pybo 질문 등록
        질문목록을 버튼을 누르면 GET방식으로 요청되어 질문 등록 화면이 나타나고,
        질문 등록 화면에서 입력값을 채우고 저장하기를 누르면 POST 방식으로 요청되어 데이터가 저장된다.
        form.is_valid 함수는 POST 요청으로 받은 form이 유효한지 검사한다.
        form.save 에서 commit=False는 임시저장을 얘기한다. 즉 실제 데이터는 아직 저장되지 않은 상태를 말한다.
    """
    if request.method =='POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user #추가한 속성 author 적용
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
     pybo 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        #messages 모듈은 장고가 제공하는 함수로 오류를 임의로 발생시키고 싶은 경우에 사용한다.
        #이때 임의로 발생시킨 오류는 폼필드와 관련이 없으므로 넌필드 오류에 해당된다.
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id= question_id)

    if request.method =="POST":
        #POST 요청으로 수정 내용을 반영하는 경우에는 다음과 같은 폼을 생성해야한다.
        #아래 코드는 question을 기본값으로 하여 화면으로 전달받은 입력값들을 덮어써서 QuestionForm을 생성하라는 의미.
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        #GET 요청으로 질문 수정 화면이 나타날 때 기존에 저장되어 있던 제목, 내용이 반영된 상태에서
        #수정을 시작할 수 있도록 다음과 같이 폼을 생성했다.
        #이처럼 instance 매개변수에 question을 지정하면 기존 값을 폼에 채울 수 있다.
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
        pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author :
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)
    question.delete()
    return redirect('pybo:index')
