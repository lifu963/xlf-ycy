from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import MessageForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import DefenderForm
from .models import Defender, Message
from .utils import get_defender_key, randSaying, clearSayings
import random


# Create your views here.

def defender(request):
    key = get_defender_key(request)
    if not request.COOKIES.get(key):
        context = {}
        m_defender = Defender.objects.all().order_by("-stars")[0]
        context['defender'] = m_defender
        defender_form = DefenderForm()
        context['defender_form'] = defender_form
        sayings = randSaying()
        if sayings!=None:
          context['author'] = sayings.author
          context['sayings'] = clearSayings(sayings.content)
        else:
            context['author'] = None
            context['sayings']=None
        return render(request, 'treehole/defender.html', context)
    return redirect(reverse('tree') + '?from=' + request.path)


def defender_for_medal(request):
    key = get_defender_key(request)
    defender_form = DefenderForm(request.POST, user=request.user)
    data = {}
    if defender_form.is_valid():
        data['status'] = 'SUCCESS'
        age = 24 * 60 * 60
        response = JsonResponse(data)
        response.set_cookie(key, 'true', age)
    else:
        data['status'] = 'ERROR'
        response = JsonResponse(data)
    return response


def update_message(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    message_form = MessageForm(request.POST, user=request.user)
    data = {}
    if message_form.is_valid():
        # 保存到数据库
        message = Message()
        message.author = request.user
        message.content = message_form.cleaned_data['text']
        message.save()

        # ajax留言更新
        data['status'] = "SUCCESS"
        data['username'] = request.user.get_nickname_or_username()
        data['message_time'] = message.create_time.timestamp()
        if len(message.content) <= 12:
            data['text'] = message.content
        else:
            data['text'] = message.content[:12]
        data['pk'] = message.pk
    else:
        return render(request, 'error.html', {'message': message_form.errors, 'redirect_to': referer})
        data['status'] = "ERROR"
        data['error_message'] = list(message_form.errors.values())[0][0]
    return JsonResponse(data)


def tree(request):
    key = get_defender_key(request)
    if not request.COOKIES.get(key):
        # 若没获取到cookie,则返回到首页
        return redirect(reverse('home'))
    # 若获取到cookie,发现不是从城门进入，返回到首页
    if request.GET.get('from') != reverse('defender'):
        return redirect(reverse('home'))
    messages = Message.objects.all().order_by("-create_time")
    context = {}
    context['messages'] = messages
    message_form = MessageForm()
    context['message_form'] = message_form
    # 获取下方最新1条无根评论
    # 若评论数大于1，则...
    return render(request, 'treehole/tree.html', context)


def message_detail(request, message_pk):
    key = get_defender_key(request)
    if not request.COOKIES.get(key):
        return redirect(reverse('home'))
    if request.GET.get('from') != reverse('tree'):
        return redirect(reverse('home'))
    message = get_object_or_404(Message, pk=message_pk)
    context = {}
    context['message'] = message
    return render(request, 'treehole/message_detail.html', context)
