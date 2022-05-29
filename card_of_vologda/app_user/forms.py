from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError

from app_user.models import CustomUser


class UserCreationForm(forms.ModelForm):
    """Форма для создания нового пользователя."""

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Форма, используемая в интерфейсе администратора
    для изменения информации о пользователе и его списка прав.
    """

    password = ReadOnlyPasswordHashField(
        label='Пароль',
        help_text='Необработанные пароли не сохраняются, '
                  'поэтому нет возможности увидеть пароль этого пользователя,'
                  ' но вы можете изменить пароль с помощью '
                  '<a href="{}">этой формы</a>.',
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'is_organization', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]


class CorrectUserForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя"""

    class Meta:
        model = CustomUser
        fields = ['last_name', 'first_name', 'middle_name', 'phone', 'num_card']


class RegisterUserForm(UserCreationForm):
    """Форма для регистрации пользователя"""

    email = forms.CharField(
        label='Email *',
        widget=forms.TextInput()
    )

    first_name = forms.CharField(
        label='Имя *',
        widget=forms.TextInput()
    )

    middle_name = forms.CharField(
        label='Отчество',
        widget=forms.TextInput(),
        required=False
    )

    last_name = forms.CharField(
        label='Фамилия *',
        widget=forms.TextInput()
    )

    num_card = forms.CharField(
        label='Номер карты *',
        widget=forms.NumberInput()
    )

    password1 = forms.CharField(
        label='Пароль *',
        widget=forms.PasswordInput()
    )

    password2 = forms.CharField(
        label='Повтор пароля *',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = CustomUser
        fields = ['email',
                  'first_name',
                  'middle_name',
                  'last_name',
                  'num_card',
                  'password1',
                  'password2'
                  ]

    def clean_num_card(self):
        card = self.cleaned_data['num_card']
        if len(card) != 16:
            raise ValidationError('Номер карты должен состоять из 16 цифр')
        if not card.isdigit():
            raise ValidationError('Номер карты должен содержать только цифры')
        if CustomUser.objects.filter(num_card=int(card)).exists():
            raise ValidationError('Карта с таким номером уже зарегистрирована')
        return card
