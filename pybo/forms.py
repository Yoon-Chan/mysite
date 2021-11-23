from django import forms
from pybo.models import Question

# 장고 폼 작성하기
#ModelForm을 상속받은 QuestionForm 클래스를 작성.
#Question 클래스 안에 내부 클래스로 Meta 클래스를 작성하고, Meta 클래스 안에는 model, fields 속성을 다음과 같이 작성.
#이 같은 클래스를 장고 폼이라고 한다. forms.Form을 상속받으면 폼, forms.ModelForm을 상속받으면 모델폼이라고 한다.
#장고 모델폼은 내부 클래스로 Meta클래스를 반드시 가져야하며, Meta 클래스에는 모델 폼이 사용할 모델과 모델의 필드들을 적어야한다.

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        #폼에 부트스트랩 적용하기.
        widgets ={
            'subject' : forms.TextInput(attrs={'class' : 'form-control'}),
            'content' : forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        #label 속성 수정하여 Subject, Content 한글로 변경하기
        labels = {
            'subject' : '제목',
            'content' : '내용',
        }