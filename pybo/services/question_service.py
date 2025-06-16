from django.core.exceptions import ObjectDoesNotExist
from pybo.models import Question

class QuestionNotFound(Exception):
    pass

def get_question_by_id(question_id: int) -> Question:
    try:
        return Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise QuestionNotFound(f"Question with id={question_id} not found")

def create_question(subject: str, content: str, author) -> Question:
    question = Question(subject=subject, content=content, author=author)
    question.save()
    return question

def modify_question(question: Question, subject: str, content: str) -> Question:
    question.subject = subject
    question.content = content
    question.save()
    return question

def delete_question(question: Question) -> None:
    question.delete()
