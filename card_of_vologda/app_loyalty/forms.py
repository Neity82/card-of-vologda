from django import forms
from django.core.exceptions import ValidationError

from app_user.models import CustomUser


class VerifyForm(forms.ModelForm):
    """Форма для получения номера карты жителя"""

    num_card = forms.CharField(label='Номер карты', widget=forms.NumberInput())

    class Meta:
        model = CustomUser
        fields = ['num_card']

    def clean_num_card(self):
        card = self.cleaned_data['num_card']
        if len(card) != 16:
            raise ValidationError('Номер карты должен состоять из 16 цифр')
        if not card.isdigit():
            raise ValidationError('Номер карты должен содержать только цифры')
        return card


class AccrueForm(forms.ModelForm):
    """Форма для начисления бонусов жителю"""
    class Meta:
        model = CustomUser
        fields = ['num_card', 'balance']


class ApplicationForm(forms.Form):
    """
    Форма-заявка для организации,
    желающей присоединиться к программе
    для отправки на email
    """

    email = forms.EmailField(label='Email *')
    name_organization = forms.CharField(label='Название организации *')
    inn_organization = forms.CharField(label='ИНН организации *')
    phone = forms.CharField(label='Контактный телефон *')
    username = forms.CharField(label='ФИО контактного лица *')

