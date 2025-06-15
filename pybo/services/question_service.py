from django.core.exceptions import ObjectDoesNotExist
from pybo.models import Question

class QuestionNotFound(Exception):
    """ID로 조회된 질문이 없을 때 발생시킬 예외"""
    pass

def get_question_by_id(question_id: int) -> Question:
    """
    주어진 question_id로 Question 객체를 조회.
    없으면 QuestionNotFound 예외 발생.
    """
    try:
        return Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise QuestionNotFound(f"Question with id={question_id} not found")

def create_question(subject: str, content: str, author) -> Question:
    """
    새 질문을 생성하여 반환.
    """
    question = Question(subject=subject, content=content, author=author)
    question.save()
    return question

def modify_question(question: Question, subject: str, content: str) -> Question:
    """
    기존 Question을 수정하고 반환.
    """
    question.subject = subject
    question.content = content
    question.save()
    return question

def delete_question(question: Question) -> None:
    """
    Question을 삭제.
    """
    question.delete()
