# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

from django import forms
from django.core.exceptions import ValidationError


class AddFaceForm(forms.Form):
    photo = forms.ImageField(label='Фото')
    name = forms.CharField(label='Имя')


class FindFaceForm(forms.Form):
    photo = forms.ImageField(label='Выберите файл с фотографией...', required=False)
    url = forms.CharField(label='...или введите URL', required=False)

    n = forms.IntegerField(label='Максимальное количество найденных фотографий', required=True, min_value=1,
                           max_value=50, initial=10)

    threshold = forms.ChoiceField(
        label='Требуемая точность поиска', required=True,
        choices= [
            ['strict', 'Высокая'],
            ['medium', 'Средняя'],
            ['low', 'Низкая'],
        ],
        initial='medium'
    )


    def clean(self):
        check = [self.cleaned_data['photo'], self.cleaned_data['url']]
        if any(check) and not all(check):
            return self.cleaned_data
        raise ValidationError('Выберите файл или URL')
