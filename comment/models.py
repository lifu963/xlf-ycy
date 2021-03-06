from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import threading
from django.template.loader import render_to_string

class SendEmail(threading.Thread):
     def __init__(self,subject,text,email,fail_silently=False):
          self.subject = subject
          self.text = text
          self.email = email
          self.fail_silently = fail_silently
          threading.Thread.__init__(self)

     def run(self):
          send_mail(self.subject, '', settings.EMAIL_HOST_USER, [self.email],self.fail_silently,html_message=self.text)

# Create your models here.
class Comment(models.Model):
     content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
     object_id=models.PositiveIntegerField()
     content_object=GenericForeignKey('content_type','object_id')

     text=models.TextField()
     comment_time=models.DateTimeField(auto_now_add=True)
     user=models.ForeignKey(User,related_name="comments",on_delete=models.CASCADE)

     root=models.ForeignKey('self',null=True,related_name='root_comment',on_delete=models.CASCADE)
     parent=models.ForeignKey('self',null=True,blank=True,related_name="parent_comment",on_delete=models.CASCADE)
     reply_to=models.ForeignKey(User,null=True,blank=True,related_name='replies',on_delete=models.CASCADE)

     def send_email(self):
          # 发送邮件通知
          if self.parent is None:
               # 评论博客
               subject = '有人评论了你的博客'
               email = self.content_object.get_email()
          else:
               # 回复评论
               subject = '有人回复了你的评论'
               email = self.reply_to.email
          if email != '':
               context={}
               context['comment_text'] = self.text
               context['url'] = self.content_object.get_url()
               text = render_to_string('comment/send_email.html',context)
               email_send = SendEmail(subject,text,email)
               email_send.start()


     def __str__(self):
          return self.text

     class Meta:
          ordering=['comment_time']