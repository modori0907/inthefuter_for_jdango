# 登録画面や入力画面を作成するために新規追加した
from django import forms

from .models import Patchs, Comment


class PatchForm(forms.ModelForm):
    # 選択式で表示させるために
    application_choices = [('ACM', 'ACM'), ('CMS', 'CMS'), ('AES', 'AES'), ('SMGR', 'SMGR')]

    name = forms.ChoiceField(choices=application_choices,
                             widget=forms.Select(attrs={'class': 'form-control'}))

# ここを更新しないとupdateで表示したときに整列して表示されない
    class Meta:
        model = Patchs
        # fields = '__all__'
        # 全部のフィールドが表示されないようにする。ここに指定した順に表示される
        fields = ['name', 'release_date', 'name']


        widgets = {
            'checks': forms.TextInput(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'patch_name': forms.Textarea(attrs={'class': 'form-control'}),
            'patch_no': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_url': forms.URLInput(attrs={'class': 'form-control'}),
            'patch_no': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_url': forms.URLInput(attrs={'class': 'form-control'}),
            'Notes': forms.URLInput(attrs={'class': 'form-control'}),
            'Remark': forms.URLInput(attrs={'class': 'form-control'}),

        }

# コメント追加用
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text')