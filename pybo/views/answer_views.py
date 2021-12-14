from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import request

from ..models import Question,Answer
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from ..forms import AnswerForm
from django.contrib.auth.decorators import  login_required
from django.contrib import messages

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
        pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author= request.user #추가한 속성 author 적용
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question_id),answer.id))
            #redirect('pybo:detail', question_id=question_id)
            # 앵커 엘리먼트를 포함하기위한 변경
    else:
        form = AnswerForm()
    context = {'question' : question, 'form' : form}
    return render(request,'pybo/question_detail.html',context)

    #answer_set은 Answer 모델이 Question 모델을 Foreign Key로 참조하고 있으므로 question.answer_set 같은 표현을 사용할 수 있다.
    #request.POST.get('content')는 name이 content인 값을 의미. POST 형식으로 전송된 form 데이터 항목을 부름.
    #question.answer_set.create(content=request.POST.get('content'),
    #                           create_date = timezone.now())
    #redirect함수는 함수에 전달된 값을 참고하여 페이지 이동을 수행.
    # 1번째 인수는 이동할 페이지의 별칭, 2번째 인수는 해당 URL에 전달해야하는 값을 입력.
    #return redirect('pybo:detail', question_id = question_id)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
        pybo 답변 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id = answer.question_id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail',question_id=answer.question.id),answer.id
            ))
            #앵커 엘리먼트를 위한 redirect 변경
            #redirect('pybo:detail', question_id = answer.question_id)

    else:
        form = AnswerForm(instance=answer)
    context = {'answer' :answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
        답변 삭제
    """
    answer = get_object_or_404(Answer, pk= answer_id)
    if request.user != answer.author:
        messages.error(request,'삭제 권한이 없습니다.')
        return  redirect('pybo:detail', question_id=answer.question.id)

    else:
        answer.delete()
    return redirect('pybo:detail', question_id= answer.question.id)
