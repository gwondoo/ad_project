from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse, HttpResponse, FileResponse
from ..forms import QuestionForm
from ..models import Question
from pybo.services.question_service import (
    get_question_by_id,
    create_question,
    modify_question,
    delete_question,
    QuestionNotFound,
)


def question_list(request):
    questions = Question.objects.order_by('-create_date')
    return render(request, 'pybo/question_list.html', {'question_list': questions})


def question_detail(request, question_id):
    try:
        question = get_question_by_id(question_id)
    except QuestionNotFound:
        return HttpResponse('질문을 찾을 수 없습니다', status=404)

    data = {
        'method': request.method,
        'get_params': request.GET.dict(),
        'user_agent': request.META.get('HTTP_USER_AGENT'),
        'absolute_url': request.build_absolute_uri(),
    }
    return JsonResponse(data)


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            question = create_question(
                subject=data['subject'],
                content=data['content'],
                author=request.user
            )
            attachment = request.FILES.get('attachment')
            if attachment:
                question.attachment.save(attachment.name, attachment)
            request.session['last_qid'] = question.pk
            response = redirect('pybo:index')
            response.set_cookie('last_qid', question.pk)
            return response
    else:
        form = QuestionForm()
    last_qid = request.session.get('last_qid')
    cookie_qid = request.COOKIES.get('last_qid')
    return render(request, 'pybo/question_form.html', {'form': form, 'last_qid': last_qid, 'cookie_qid': cookie_qid})


@login_required(login_url='common:login')
def question_modify(request, question_id):
    try:
        question = get_question_by_id(question_id)
    except QuestionNotFound:
        return HttpResponse('질문을 찾을 수 없습니다', status=404)

    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            data = form.cleaned_data
            question = modify_question(
                question,
                subject=data['subject'],
                content=data['content']
            )
            attachment = request.FILES.get('attachment')
            if attachment:
                question.attachment.save(attachment.name, attachment)
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'pybo/question_form.html', {'form': form})


@login_required(login_url='common:login')
def question_delete(request, question_id):
    try:
        question = get_question_by_id(question_id)
    except QuestionNotFound:
        return HttpResponse('질문을 찾을 수 없습니다', status=404)

    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    delete_question(question)
    return HttpResponse(status=204)


def download_attachment(request, question_id):
    try:
        question = get_question_by_id(question_id)
    except QuestionNotFound:
        return HttpResponse('질문을 찾을 수 없습니다', status=404)
    attachment = getattr(question, 'attachment', None)
    if not attachment:
        return HttpResponse(status=204)
    file_handle = attachment.open('rb')
    return FileResponse(file_handle, as_attachment=True, filename=attachment.name)
