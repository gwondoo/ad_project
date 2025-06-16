from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from pybo.models import Answer, Question

class AnswerNotFound(Exception):
    pass


def get_answer_by_id(answer_id: int) -> Answer:
    try:
        return Answer.objects.get(pk=answer_id)
    except Answer.DoesNotExist:
        raise AnswerNotFound(f"Answer with id={answer_id} not found")


def create_answer(question_id: int, content: str, author) -> Answer:
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
    answer.content = content
    answer.modify_date = timezone.now()
    answer.save()
    return answer


def delete_answer(answer: Answer) -> None:
    answer.delete()
