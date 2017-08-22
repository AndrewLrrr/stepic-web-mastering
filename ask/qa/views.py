from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET

from .models import Question
from .forms import AskForm, AnswerForm


PAGINATION_LIMIT = 100
ITEMS_PER_PAGE = 10


@require_GET
def new_questions(request):
    questions = Question.objects.new()
    return paginated_list(request, questions, 'new', 'questions')


@require_GET
def popular_questions(request):
    questions = Question.objects.popular()
    return paginated_list(request, questions, 'popular', 'questions')


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': question.pk})
    return render(request, 'question_detail.html', {
        'question': question,
        'form': form
    })


def question_ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'question_ask.html', {'form': form})


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def paginated_list(request, qs, prefix, name):
    name = '{}_{}'.format(prefix, name)
    try:
        limit = int(request.GET.get('limit', ITEMS_PER_PAGE))
    except ValueError:
        limit = ITEMS_PER_PAGE
    if limit > PAGINATION_LIMIT:
        limit = ITEMS_PER_PAGE
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    paginator.url = '{}?page='.format(reverse(name))
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request, '{}.html'.format(name), {
        'paginator': paginator,
        'page': page,
        'qs': page.object_list,
    })
