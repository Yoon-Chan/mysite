from ..models import Question
from django.shortcuts import render, get_object_or_404


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