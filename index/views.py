from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from datetime import datetime, timedelta

from random import randint
from django.utils.text import slugify
from django.core.paginator import Paginator
from .forms import MyForm

def index(request):
    http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if http_x_forwarded_for:
        ip = http_x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if BlockedIP.objects.filter(ip=ip).exists():
        return HttpResponse('IP banned')

    latestQuestions = Question.objects.all().order_by('-timestamp')

    return render(request, 'index/index.html', {'latestQuestions': latestQuestions[:10]})

def question(request, id, slug):
    http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if http_x_forwarded_for:
        ip = http_x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if BlockedIP.objects.filter(ip=ip).exists():
        return HttpResponse('IP banned')

    question = Question.objects.get(id=id)

    if not question.slug == slug[:255]:
        return redirect('index')

    question.questionViews = question.questionViews + 1
    question.save()
    comment = Comment.objects.filter(questionId=id).order_by('timestamp')

    randomNumber = randint(10,20)
    randomNumberModified = randomNumber - 10
    otherQuestions = Question.objects.all()[randomNumberModified:randomNumber]
    form = MyForm()
    return render(request, 'index/question.html', {'question':question, 'comment':comment, 'otherQuestions':otherQuestions, 'form':form})

def randomQuestion(request):
    countQuestions = Question.objects.count() - 1
    randomNumber = randint(0, countQuestions)
    qna = Question.objects.filter()[randomNumber]

    http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if http_x_forwarded_for:
        ip = http_x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if BlockedIP.objects.filter(ip=ip).exists():
        return HttpResponse('IP banned')

    question = Question.objects.get(id=qna.id)


    question.questionViews = question.questionViews + 1
    comment = Comment.objects.filter(questionId=qna.id)

    randomNumber = randint(10, 1200)
    randomNumberModified = randomNumber - 10
    otherQuestions = Question.objects.all()[randomNumberModified:randomNumber]

    return render(request, 'index/randomQuestion.html', {'question': question, 'comment': comment, 'otherQuestions': otherQuestions})

def search(request):
    query = request.GET['q']
    if query.replace(' ', '') == '':
        return redirect('index')
    question = Question.objects.filter(questionTitle__icontains=query)
    return render(request, 'index/search.html', {'question': question})

def changelog(request):
    return render(request, 'index/changelog.html')

def stats(request):
    getViews = Question.objects.all().order_by('-questionViews').values_list('questionTitle', 'questionViews')[:10]
    return HttpResponse(getViews)


def infiniteScroll(request):
    latestQuestions = Question.objects.all().order_by('-timestamp')

    #paginator
    paginator = Paginator(latestQuestions, 10)
    pageNumber = request.GET.get('page')
    latestQuestions = paginator.get_page(pageNumber)
    return render(request, 'index/infiniteScroll.html', {'latestQuestions': latestQuestions})

def postQuestion(request):
    if request.POST['questionTitle']:
        questionTitle = request.POST['questionTitle'][:450].strip()
        questionTitle = questionTitle[0].upper() + questionTitle[1:]
        questionLength = len(questionTitle)
        if not questionLength < 5:
            slugTitle = slugify(questionTitle)
            if slugTitle == '':
                return redirect('index')

            if questionTitle.endswith('.') == True:
                questionTitle = questionTitle[:-1]

            if questionTitle.endswith('?') == False:
                questionTitle = str(questionTitle) + '?'

            http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if http_x_forwarded_for:
                ip = http_x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            if Question.objects.filter(timestamp__date=datetime.today(), ip=ip).count() >= 15:
                return HttpResponse('You have reached your daily limit.')

            slugTitle = slugTitle[:255]
            question = Question(questionTitle=questionTitle, ip=ip, slug=str(slugTitle))
            question.save()
            return redirect('question', str(question.id), str(slugTitle)) #Change slugtitle to question.slug
        return redirect('index')
    else:
        return redirect('index')

def postComment(request, id):
    commentText = request.POST['commentText'].strip()
    if "http://" in commentText or "https://" in commentText:
        return HttpResponse("No links allowed")
    question = Question.objects.get(id=id)
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            if not len(commentText) == 0:
                http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if http_x_forwarded_for:
                    ip = http_x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')

                if Comment.objects.filter(timestamp__date=datetime.today(), ip=ip).count() >= 40:
                    return HttpResponse('You have reached your daily limit.')

                Comment(questionId=question, commentText=commentText, ip=ip).save()
                return redirect('question', str(question.id), str(question.slug))
            return redirect('question', str(question.id), str(question.slug))
        else:
            return redirect('question', str(question.id), str(question.slug))