from ..models import Question
from django.shortcuts import render, get_object_or_404
from django.db.models import Q,Count


#페이지 기능 구현하기 위한 사용 모듈
from django.core.paginator import  Paginator

# Create your views here.
def index(request):
    # pybo 목록 출력(Question)

    #입력 인자
    page = request.GET.get('page', '1') #페이지
    kw = request.GET.get('kw', '')      #검색어
    so = request.GET.get('so', 'recent')#정렬 기준
    
    #정렬
    if so == 'recommend':
        question_list =Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    elif so == 'recent': #recent
        question_list= Question.objects.order_by('-create_date')
    
    #조회
    #question_list = Question.objects.order_by('-create_date') 정렬기능을 작성하였으므로 삭제
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |                      #제목 검색
            Q(content__icontains=kw) |                      #내용 검색
            Q(author__username__icontains=kw) |             #질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)       #답변 글쓴이 검색
        ).distinct()

    #페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    #리스트 내용
    context = {'question_list' : page_obj, 'page':page, 'kw':kw}#question_list} #page와 kw 추가.

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