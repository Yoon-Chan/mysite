from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#pybo/models.py 에 질문 모델 작성하기.

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author= models.ForeignKey(User, on_delete=models.CASCADE)#,null="True) 이것은 글쓴이가 null을 포함할 경우.
    #ForeignKey 는 쉽게 말해 다른 모델과의 연결을 의미하며, on_delete = models.CASCADE는 답변에 연결된 질문이
    #삭제되면 답변도 함께 삭제하라는 의미.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
