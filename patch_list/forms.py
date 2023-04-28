# 登録画面や入力画面を作成するために新規追加した
from django import forms
from .models import Patchs

# class PatchForm(forms.ModelForm):
#     # application_choices = [('ACM', 'ACM'), ('CMS', 'CMS'), ('AES', 'AES'), ('SMGR', 'SMGR')]
#     class Meta:
#         model = Patchs
#         fields = '__all__'
#         #
#         widgets = {
#             # 'class': 'form-control'は入力行間を広くするため
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             # 'name': forms.ChoiceField(choices=(('ACM', 'ACM'), ('CMS', 'CMS'), ('AES', 'AES'), ('SMGR', 'SMGR')),
#             #                           widget=forms.Select(attrs={'class': 'form-control'})),
#             'checks': forms.TextInput(attrs={'class': 'form-control'}),
#             # 年月日をGUIで指定できるように。
#             'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             # Textareaは複数行入力出来るように
#             'patch_name': forms.Textarea(attrs={'class': 'form-control'}),
#             'patch_no': forms.TextInput(attrs={'class': 'form-control'}),
#             'reference_url': forms.URLInput(attrs={'class': 'form-control'}),
#         }

class PatchForm(forms.ModelForm):
    application_choices = [('ACM', 'ACM'), ('CMS', 'CMS'), ('AES', 'AES'), ('SMGR', 'SMGR')]

    name = forms.ChoiceField(choices=application_choices,
                             widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Patchs
        fields = '__all__'
        widgets = {
            'checks': forms.TextInput(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'patch_name': forms.Textarea(attrs={'class': 'form-control'}),
            'patch_no': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


