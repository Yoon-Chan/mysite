from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#pybo/models.py 에 질문 모델 작성하기.

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    #modify_date 필드 추가하기 Question과 Answer 모델에 수정일시를 의미하는 것.
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author= models.ForeignKey(User, on_delete=models.CASCADE)#,null="True) 이것은 글쓴이가 null을 포함할 경우.
    #ForeignKey 는 쉽게 말해 다른 모델과의 연결을 의미하며, on_delete = models.CASCADE는 답변에 연결된 질문이
    #삭제되면 답변도 함께 삭제하라는 의미.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    # modify_date 필드 추가하기
    # null=True는 데이터베이스에서 modify_date 칼럼에 null을 허용한다는 의미
    # blank= True는 Form.is_valid()를 통한 입력 폼 데이터 검사 시 값이 없어도 된다는 의미이다.
    modify_date = models.DateTimeField(null=True, blank=True)

#답변 클래스, Question or Answer 필드 중 하나에만 값이 저장되므로 두 필드는 모두
#null =True, blank =True여야 한다.
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True,
                                 on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)

