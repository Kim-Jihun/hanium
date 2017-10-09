from django import forms

def min_length_1_validator(value):
    if len(value)<1:
        raise forms.ValidationError('1글자 이상 입력해주세요')

