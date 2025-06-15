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


from pybo.models import Question, Answer, Comment  # 필요시 import 추가
from django.utils import timezone

def create_comment(question_id=None, answer_id=None, content=None, author=None) -> Comment:
    """
    질문 또는 답변에 댓글 생성.
    하나는 반드시 지정해야 하며, 둘 다 None이면 ValueError 발생.
    """
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
