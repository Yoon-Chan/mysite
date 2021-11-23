from django.urls import path

from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name = 'index'),
    #URL 매핑을 통하여 질문 목록 보여주기
    path('<int:question_id>/', views.detail, name = 'detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
]