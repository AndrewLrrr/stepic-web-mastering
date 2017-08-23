from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.decorators.http import require_GET

from .models import Question
from .forms import AskForm, AnswerForm, UserSingUpForm, UserLoginForm


PAGINATION_LIMIT = 100
ITEMS_PER_PAGE = 10


@require_GET
def new_questions(request):
    questions = Question.objects.new()
    return paginated_list(request, questions, 'new_questions', 'qa:index')


@require_GET
def popular_questions(request):
    questions = Question.objects.popular()
    return paginated_list(request, questions, 'popular_questions', 'qa:popular')


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.save()
            url = question.get_url()
            return redirect(url)
    else:
        form = AnswerForm(initial={'question': question.pk})
    return render(request, 'question_detail.html', {
        'question': question,
        'form': form
    })


@login_required
def question_ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            url = question.get_url()
            return redirect(url)
    else:
        form = AskForm()
    return render(request, 'question_ask.html', {'form': form})


def user_singup(request):
    if request.user.is_authenticated():
        return redirect('qa:index')
    if request.method == 'POST':
        form = UserSingUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('qa:index')
    else:
        form = UserSingUpForm()
    return render(request, 'singup.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated():
        return redirect('qa:index')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('qa:index')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('qa:index')


def paginated_list(request, qs, template, route):
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
    paginator.url = '{}?page='.format(reverse(route))
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request, '{}.html'.format(template), {
        'paginator': paginator,
        'page': page,
        'qs': page.object_list,
    })
