from django.contrib import admin
from .models import Question

# Register your models here.



#장고 Admin에 데이터 검색 기능 추가하기
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

#장고 admin에 Question 모델 추가하기.
admin.site.register(Question,QuestionAdmin)