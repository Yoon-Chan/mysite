from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.decorators import  login_required

#페이지 기능 구현하기 위한 사용 모듈
from django.core.paginator import  Paginator

# Create your views here.
def index(request):
    # pybo 목록 출력(Question)

    #입력 인자
    page = request.GET.get('page', '1') #페이지

    #조회
    question_list = Question.objects.order_by('-create_date')

    #페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    #리스트 내용
    context = {'question_list' : page_obj}#question_list}

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
            return redirect('pybo:detail', question_id=question_id)
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