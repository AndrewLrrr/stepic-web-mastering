from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET

from .models import Question


ITEMS_PER_PAGE = 10


@require_GET
def new_questions(request):
    questions = Question.objects.new()
    return paginated_list(request, questions, 'new', 'questions')


@require_GET
def popular_questions(request):
    questions = Question.objects.popular()
    return paginated_list(request, questions, 'popular', 'questions')


@require_GET
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'question_detail.html', {'question': question})


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def paginated_list(request, qs, prefix, name):
    name = '{}_{}'.format(prefix, name)
    limit = request.GET.get('limit', ITEMS_PER_PAGE)
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, limit)
    paginator.url = '{}?page='.format(reverse(name))
    page = paginator.page(page)
    return render(request, '{}.html'.format(name), {
        'paginator': paginator,
        'page': page,
        'qs': page.object_list,
    })


def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', ITEMS_PER_PAGE))
    except ValueError:
        limit = ITEMS_PER_PAGE
    if limit > 100:
        limit = ITEMS_PER_PAGE
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page
