from pybo.models import Question, Answer

class QuestionNotFound(Exception):
    """ID로 조회된 질문이 없을 때 발생시킬 예외"""
    pass

class AnswerNotFound(Exception):
    """ID로 조회된 답변이 없을 때 발생시킬 예외"""
    pass

class CannotVoteOwnQuestion(Exception):
    """본인 작성 질문에 추천 시도 시 발생할 예외"""
    pass

class CannotVoteOwnAnswer(Exception):
    """본인 작성 답변에 추천 시도 시 발생할 예외"""
    pass

class AlreadyVoted(Exception):
    """이미 추천한 경우 발생시킬 예외"""
    pass


def vote_question_service(question_id: int, user):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise QuestionNotFound(f"Question with id={question_id} not found")
    if question.author == user:
        raise CannotVoteOwnQuestion("Cannot vote for your own question")
    if question.voter.filter(pk=user.pk).exists():
        raise AlreadyVoted("You have already voted this question")
    question.voter.add(user)
    return question


def vote_answer_service(answer_id: int, user):
    try:
        answer = Answer.objects.get(pk=answer_id)
    except Answer.DoesNotExist:
        raise AnswerNotFound(f"Answer with id={answer_id} not found")
    if answer.author == user:
        raise CannotVoteOwnAnswer("Cannot vote for your own answer")
    if answer.voter.filter(pk=user.pk).exists():
        raise AlreadyVoted("You have already voted this answer")
    answer.voter.add(user)
    return answer
