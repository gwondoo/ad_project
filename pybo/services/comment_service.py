# pybo/services/comment_service.py

from django.utils import timezone
from pybo.models import Comment, Question

class CommentNotFound(Exception):
    """ID로 조회된 댓글이 없을 때 발생시킬 예외"""
    pass


def get_comment_by_id(comment_id: int) -> Comment:
    """
    주어진 comment_id로 Comment 객체를 조회.
    없으면 CommentNotFound 예외 발생.
    """
    try:
        return Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        raise CommentNotFound(f"Comment with id={comment_id} not found")


def create_comment(question_id: int, content: str, author) -> Comment:
    """
    주어진 question_id에 새로운 Comment 생성.
    질문이 없으면 CommentNotFound 예외 발생.
    """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise CommentNotFound(f"Question with id={question_id} not found")

    comment = Comment(
        question=question,
        content=content,
        author=author,
        create_date=timezone.now()
    )
    comment.save()
    return comment


def modify_comment(comment: Comment, content: str) -> Comment:
    """
    기존 Comment를 수정하고 반환.
    """
    comment.content = content
    comment.modify_date = timezone.now()
    comment.save()
    return comment


def delete_comment(comment: Comment) -> None:
    """
    Comment를 삭제.
    """
    comment.delete()
