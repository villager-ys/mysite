from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget


class CommentsForm(forms.Form):
    object_id = forms.CharField(widget=forms.HiddenInput)
    content_type = forms.CharField(widget=forms.HiddenInput)
    comment = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
                              error_messages={'required': '评论内容不能为空'})

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentsForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 验证user是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')

        object_id = self.cleaned_data['object_id']
        content_type = self.cleaned_data['content_type']
        # 验证评论对象
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(id=object_id)
            self.cleaned_data['model_obj'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在！！！')
        return self.cleaned_data
