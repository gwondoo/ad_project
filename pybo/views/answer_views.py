from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from ..forms import AnswerForm
from pybo.services.answer_service import (
    get_answer_by_id,
    create_answer,
    modify_answer,
    delete_answer,
    AnswerNotFound,
)


@login_required(login_url='common:login')
def answer_create(request, question_id):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                answer = create_answer(
                    question_id=question_id,
                    content=data['content'],
                    author=request.user
                )
            except Exception as e:
                messages.error(request, '답변 생성 중 오류가 발생했습니다.')
                return redirect('pybo:detail', question_id=question_id)
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = AnswerForm()
    return render(request, 'pybo/answer_form.html', {'form': form})


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    try:
        answer = get_answer_by_id(answer_id)
    except AnswerNotFound:
        return render(request, 'errors/answer_not_found.html', status=404)

    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            data = form.cleaned_data
            answer = modify_answer(
                answer,
                content=data['content']
            )
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    return render(request, 'pybo/answer_form.html', {'form': form})


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    try:
        answer = get_answer_by_id(answer_id)
    except AnswerNotFound:
        return render(request, 'errors/answer_not_found.html', status=404)

    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    delete_answer(answer)
    return redirect('pybo:detail', question_id=answer.question.id)
