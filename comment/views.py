from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .models import Comment
from .forms import CommentForm
from django.http import JsonResponse
# Create your views here.

def update_comment(request):
    referer=request.META.get('HTTP_REFERER',reverse('home'))
    comment_form=CommentForm(request.POST,user=request.user)
    data = {}
    if comment_form.is_valid():
        comment=Comment()
        comment.user=request.user
        comment.text=comment_form.cleaned_data['text']
        comment.content_object=comment_form.cleaned_data['content_object']

        parent=comment_form.cleaned_data['parent']
        if not parent is None:
            comment.parent=parent
            comment.root = parent.root if not parent.root is None else parent #若parent.root为空，则说明parent为源回复，comment.root=parent,否则，与parent.root相同
            comment.reply_to = parent.user
        comment.save()#保存到数据库

        #该comment发送邮件
        # comment.send_email()

        data['status']="SUCCESS"
        data['username']=comment.user.get_nickname_or_username()
        data['comment_time']=comment.comment_time.timestamp()
        data['text']=comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if not parent is None:#若非源回复
            data['reply_to'] =comment.reply_to.get_nickname_or_username()
        else :
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        #return render(request,'error.html',{'message':comment_form.errors,'redirect_to':referer})
        data['status']="ERROR"
        data['message']=list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
#     referer=request.META.get('HTTP_REFERER',reverse('home'))
#
# #数据检查
#     user=request.user
#     if not user.is_authenticated:
#         return render(request,'error.html',{{'message':'用户未登录!','redirect_to':referer}})
#
#     text=request.POST.get('text','').strip()
#     if text == '':
#         return render(request,'error.html',{'message':'评论内容为空!','redirect_to':referer})
#
#     try:
#         #评论对象(博客，等)
#         content_type = request.POST.get('content_type', '')
#         object_id = int(request.POST.get('object_id', ''))
#         model_class = ContentType.objects.get(model=content_type).model_class()
#         model_obj = model_class.objects.get(pk=object_id)
#
#     except Exception as e:
#         return render(request,'error.html',{'message':'评论对象不存在!','redirect_to':referer})
# #保存评论
#     comment = Comment()
#     comment.user=user
#     comment.text=text
#     comment.content_object=model_obj
#     comment.save()
#
#     referer=request.META.get('HTTP_REFERER',reverse('home'))
#     return redirect(referer)