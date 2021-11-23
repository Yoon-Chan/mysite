from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    #URL 매핑을 통하여 질문 목록 보여주기
    path('<int:question_id>/', views.detail)
]