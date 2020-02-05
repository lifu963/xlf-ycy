from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Message,Defender

class MessageForm(forms.Form):
    text=forms.CharField(widget=CKEditorWidget(config_name='message_ckeditor'),error_messages={'required':'留言内容不能为空'})

    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.user=kwargs.pop('user')
        super(MessageForm, self).__init__(*args,**kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user']=self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

class DefenderForm(forms.Form):
    question_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'defender_id','class':'navigationWrapper-li'}))
    answer = forms.CharField(label='回答',widget=forms.TextInput(attrs={'class': 'form-control navigationWrapper-li', 'placeholder': '请输入答案'}))

    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.user=kwargs.pop('user')
        super(DefenderForm, self).__init__(*args,**kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user']=self.user
        else:
            raise forms.ValidationError('用户尚未登录')

        question_id=self.cleaned_data.get('question_id',0)
        answer=self.cleaned_data.get('answer','')
        if Defender.objects.filter(pk=question_id).exists():
            defender_answer=Defender.objects.get(pk=question_id).answer
            if defender_answer != answer:
                raise forms.ValidationError('答案错误')
        else:
            raise forms.ValidationError('问答发生错误')
        return self.cleaned_data



