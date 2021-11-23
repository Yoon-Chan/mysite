from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import QuestionForm

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
    question = get_object_or_404(Question, pk=question_id) #Question.objects.get(id=question_id)
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    """
        pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    #answer_set은 Answer 모델이 Question 모델을 Foreign Key로 참조하고 있으므로 question.answer_set 같은 표현을 사용할 수 있다.
    #request.POST.get('content')는 name이 content인 값을 의미. POST 형식으로 전송된 form 데이터 항목을 부름.
    question.answer_set.create(content=request.POST.get('content'),
                               create_date = timezone.now())
    #redirect함수는 함수에 전달된 값을 참고하여 페이지 이동을 수행.
    # 1번째 인수는 이동할 페이지의 별칭, 2번째 인수는 해당 URL에 전달해야하는 값을 입력.
    return redirect('pybo:detail', question_id = question_id)


def question_create(request):
    """
        pybo 질문 등록
    """
    form = QuestionForm()
    return render(request, 'pybo/question_form.html', {'form': form})