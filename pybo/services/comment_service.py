from pybo.models import Question, Answer, Comment 
from django.utils import timezone

class CommentNotFound(Exception):
    pass


def get_comment_by_id(comment_id: int) -> Comment:
    try:
        return Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        raise CommentNotFound(f"Comment with id={comment_id} not found")


def create_comment(question_id=None, answer_id=None, content=None, author=None) -> Comment:
    if question_id is not None:
        question = Question.objects.get(pk=question_id)
        comment = Comment(
            question=question,
            content=content,
            author=author,
            create_date=timezone.now()
        )
    elif answer_id is not None:
        answer = Answer.objects.get(pk=answer_id)
        comment = Comment(
            answer=answer,
            content=content,
            author=author,
            create_date=timezone.now()
        )
    else:
        raise ValueError("question_id 또는 answer_id 중 하나는 반드시 필요합니다.")

    comment.save()
    return comment


def modify_comment(comment: Comment, content: str) -> Comment:
    comment.content = content
    comment.modify_date = timezone.now()
    comment.save()
    return comment


def delete_comment(comment: Comment) -> None:
    comment.delete()
