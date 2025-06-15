from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from pybo.models import Answer, Question

class AnswerNotFound(Exception):
    """ID로 조회된 답변이 없을 때 발생시킬 예외"""
    pass


def get_answer_by_id(answer_id: int) -> Answer:
    """
    주어진 answer_id로 Answer 객체를 조회.
    없으면 AnswerNotFound 예외 발생.
    """
    try:
        return Answer.objects.get(pk=answer_id)
    except Answer.DoesNotExist:
        raise AnswerNotFound(f"Answer with id={answer_id} not found")


def create_answer(question_id: int, content: str, author) -> Answer:
    """
    question_id에 해당하는 Question 객체에 새로운 Answer 생성.
    """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        from pybo.services.question_service import QuestionNotFound
        raise QuestionNotFound(f"Question with id={question_id} not found")

    answer = Answer(
        question=question,
        content=content,
        author=author,
        create_date=timezone.now()
    )
    answer.save()
    return answer


def modify_answer(answer: Answer, content: str) -> Answer:
    """
    기존 Answer를 수정하고 반환.
    """
    answer.content = content
    answer.modify_date = timezone.now()
    answer.save()
    return answer


def delete_answer(answer: Answer) -> None:
    """
    Answer를 삭제.
    """
    answer.delete()
