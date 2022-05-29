from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, TemplateView, CreateView, FormView, ListView

from app_loyalty.forms import VerifyForm, AccrueForm
from app_user.forms import CorrectUserForm, RegisterUserForm
from app_user.models import CustomUser, History


class LoginUser(LoginView):
    """Представление страницы для авторизации пользователя"""

    template_name = 'app_user/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Авторизация'
        return context


class СitizenAccount(DetailView):
    """Представление личного кабинета жителя"""

    model = CustomUser
    template_name = 'app_user/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Личный кабинет'
        return context


class ОrganizationAccount(DetailView):
    """Представление личного кабинета организации"""

    model = CustomUser
    template_name = 'app_user/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Личный кабинет'
        return context


class Profile(UpdateView):
    """
    Представление страницы личного кабинета жителя,
    форма изменения данных
    """

    model = CustomUser
    form_class = CorrectUserForm
    template_name = 'app_user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Профиль'
        return context


class HistoryView(ListView):
    """
    Представление страницы личного кабинета жителя,
    история начисления и списания бонусов
    """

    model = History
    template_name = 'app_user/profile.html'
    context_object_name = 'history_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'История'
        return context

    def get_queryset(self):
        return History.get_history_list(user=self.request.user)


class Verify(TemplateView):
    """
    Представление страницы личного кабинета организации,
    сервис проверки карты жителя
    """

    template_name = 'app_user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Проверить'
        context['form'] = VerifyForm
        return context

    def post(self, request, pk):
        form = VerifyForm(request.POST)
        if form.is_valid():
            card = form.cleaned_data['num_card']
            if CustomUser.objects.filter(num_card=int(card)).exists():
                card = f'{card[:4]} {card[4:8]} {card[8:12]} {card[12:16]}'
                messages.success(self.request, f'Карта {card} есть в базе', extra_tags='true')
            else:
                card = f'{card[:4]} {card[4:8]} {card[8:12]} {card[12:16]}'
                messages.success(self.request, f'Карты {card} нет в базе', extra_tags='false')

        return HttpResponseRedirect(reverse('verify', kwargs={'pk': pk}))


class Accrue(FormView):
    """
    Представление страницы личного кабинета организации,
    сервис начисления бонусов жителю
    """

    form_class = AccrueForm
    template_name = 'app_user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Начислить'
        return context

    def form_valid(self, form):
        pk = self.request.user.pk
        card = form.cleaned_data['num_card']
        card_str = f'{card[:4]} {card[4:8]} {card[8:12]} {card[12:16]}'
        if CustomUser.objects.filter(num_card=int(card)).exists():
            user = CustomUser.objects.get(num_card=int(card))
            balance = form.cleaned_data['balance']

            user.balance += int(balance)
            user.save(update_fields=['balance'])

            History.objects.create(
                user=user,
                type='Начислено',
                organization=self.request.user.organization,
                sum_points=balance
            )

            messages.success(self.request, f'На карту {card_str} начислено {balance} бонусов', extra_tags='true')
        else:
            messages.success(self.request, f'Карты {card_str} нет в базе', extra_tags='false')

        return HttpResponseRedirect(reverse('accrue', kwargs={'pk': pk}))


class Deduct(FormView):
    """
    Представление страницы личного кабинета организации,
    сервис списания бонусов жителю
    """

    form_class = AccrueForm
    template_name = 'app_user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Списать'
        return context

    def form_valid(self, form):
        pk = self.request.user.pk
        card = form.cleaned_data['num_card']
        card_str = f'{card[:4]} {card[4:8]} {card[8:12]} {card[12:16]}'
        if CustomUser.objects.filter(num_card=int(card)).exists():
            user = CustomUser.objects.get(num_card=int(card))
            balance = form.cleaned_data['balance']

            if user.balance >= int(balance):
                user.balance -= int(balance)
                user.save(update_fields=['balance'])

                History.objects.create(
                    user=user,
                    type='Списано',
                    organization=self.request.user.organization,
                    sum_points=balance
                )

                messages.success(self.request, f'С карты {card_str} списано {balance} бонусов', extra_tags='true')
            else:
                messages.success(self.request, f'На карте {card_str} не хватает бонусов для списания',
                                 extra_tags='false')
        else:
            messages.success(self.request, f'Карты {card_str} нет в базе', extra_tags='false')

        return HttpResponseRedirect(reverse('deduct', kwargs={'pk': pk}))


def password_change_done(request):
    """Изменение пароля"""

    logout(request)
    return redirect('login')


class RegisterUser(CreateView):
    """Представление страницы для регистрации пользователя"""

    form_class = RegisterUserForm
    template_name = 'app_user/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        group = Group.objects.get(name='Горожанин')
        user = form.save()
        group.user_set.add(user)
        login(self.request, user)
        return HttpResponseRedirect(reverse('home'))

