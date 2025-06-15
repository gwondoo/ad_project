from django.db import models
from django.db.models import QuerySet
from django.conf import settings
from django.contrib.auth.models import User

class Question(models.Model):
    subject     = models.CharField(max_length=200)
    content     = models.TextField()
    author      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return self.subject

    # 클래스메서드 예시 1: 전체 질문 반환
    @classmethod
    def get_all_questions(cls) -> QuerySet['Question']:
        return cls.objects.all()

    # 클래스메서드 예시 2: 최근 N개 질문 반환
    @classmethod
    def get_recent_questions(cls, n: int = 10) -> QuerySet['Question']:
        return cls.objects.order_by('-create_date')[:n]

class Answer(models.Model):
    question    = models.ForeignKey(Question, on_delete=models.CASCADE)
    content     = models.TextField()
    author      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True,auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question.id}"

    # 클래스메서드 예시: 특정 질문의 답변들 반환
    @classmethod
    def get_answers_for_question(cls, question_id: int) -> QuerySet['Answer']:
        return cls.objects.filter(question_id=question_id)

    # 함수형 예시: 답변 수 반환 (모델 메서드)
    def answer_length(self) -> int:
        return len(self.content)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    # 질문 또는 답변에 연결될 수 있음
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20]