from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..models import Question, Answer
from pybo.services.vote_service import (
    vote_question_service,
    vote_answer_service,
    QuestionNotFound,
    AnswerNotFound,
    CannotVoteOwnQuestion,
    CannotVoteOwnAnswer,
    AlreadyVoted,
)


@login_required(login_url='common:login')
def vote_question(request, question_id):
    try:
        vote_question_service(question_id, request.user)
    except QuestionNotFound:
        return render(request, 'errors/question_not_found.html', status=404)
    except CannotVoteOwnQuestion:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    except AlreadyVoted:
        messages.error(request, '이미 추천했습니다')
    return redirect('pybo:detail', question_id=question_id)


@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    from pybo.models import Answer  

    try:
        answer = vote_answer_service(answer_id, request.user)
        return redirect('pybo:detail', question_id=answer.question.id)

    except CannotVoteOwnAnswer:
        answer = Answer.objects.get(pk=answer_id)
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    except AlreadyVoted:
        answer = Answer.objects.get(pk=answer_id)
        messages.error(request, '이미 추천했습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    except AnswerNotFound:
        return render(request, 'errors/answer_not_found.html', status=404)
