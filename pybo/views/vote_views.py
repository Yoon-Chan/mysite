from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect

from ..models import Question,Answer


# ManyToManyFeild는 같은사용자가 하나의 질문을 여러 번 추천해도 추천 수가 증가하지 않는다.
# 중복을 허락하지 않기 때문.
@login_required(login_url='common:login')
def vote_question(request, question_id):
    """
        pybo 질문 추천 등록
    """

    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request,'본인이 작성한 글은 추천할 수 없습니다.')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question_id)

@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    """
        pybo 답변 추천 등록
    """
    answer = get_object_or_404(Answer, pk= answer_id)
    if request.user == answer.author:
        messages.error(request,'본인이 작성한 글은 추천할 수 없습니다.')
    else:
        answer.voter.add(request.user)
    return redirect('pybo:detail', question_id = answer.question.id)

