from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..forms import CommentForm
from pybo.services.comment_service import (
    get_comment_by_id,
    create_comment,
    modify_comment,
    delete_comment,
    CommentNotFound,
)

@login_required(login_url='common:login')
def comment_create(request, question_id):
    """
    pybo 댓글등록
    """
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                create_comment(question_id=question_id, content=data['content'], author=request.user)
            except CommentNotFound:
                return render(request, 'errors/question_not_found.html', status=404)
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = CommentForm()
    return render(request, 'pybo/comment_form.html', {'form': form})

@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    """
    pybo 댓글수정
    """
    try:
        comment = get_comment_by_id(comment_id)
    except CommentNotFound:
        return render(request, 'errors/comment_not_found.html', status=404)

    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            data = form.cleaned_data
            modify_comment(comment, content=data['content'])
            return redirect('pybo:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'pybo/comment_form.html', {'form': form})

@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    """
    pybo 댓글삭제
    """
    try:
        comment = get_comment_by_id(comment_id)
    except CommentNotFound:
        return render(request, 'errors/comment_not_found.html', status=404)

    if request.user != comment.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)

    delete_comment(comment)
    return redirect('pybo:detail', question_id=comment.question.id)
