from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView

from app_loyalty.forms import ApplicationForm
from app_loyalty.models import News, Discount
from config.settings import DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL


class Home(ListView):
    """
    Представление главной страницы.

    - список новостей
    - переход на заявку на участие в программе
    """

    model = News
    template_name = 'app_loyalty/index.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        return News.get_news_list(limit=5)


class NewsList(ListView):
    """Представление страницы с новостями"""

    paginate_by = 10
    model = News
    template_name = 'app_loyalty/news.html'
    context_object_name = 'news_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Новости'
        return context

    def get_queryset(self):
        return News.get_news_list()


class NewsDetail(DetailView):
    """Представление детальной страницы новости"""

    model = News
    template_name = 'app_loyalty/news_detail.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Новости'
        return context


class DiscountList(ListView):
    """Представление страницы со скидками партнеров"""

    model = Discount
    template_name = 'app_loyalty/discount.html'
    context_object_name = 'discount_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Партнеры'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Discount.get_discount_list()


class DiscountCategory(ListView):
    """Представление списка скидок в выбранной категории"""

    model = Discount
    template_name = 'app_loyalty/discount.html'
    context_object_name = 'discount_list'
    allow_empty = False

    def get_queryset(self):
        return Discount.get_discount_list(category_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['discount_list'][0].organization.category)
        context['cat_selected'] = context['discount_list'][0].organization.category_id
        return context


def about_project(request):
    return render(request, 'app_loyalty/about.html', {'title': 'О проекте'})


class Application(FormView):
    """
    Представление страницы для отправки заявки
    на присоединение к программе
    """

    form_class = ApplicationForm
    template_name = 'app_loyalty/application.html'

    def form_valid(self, form):
        subject = 'Заявка на присоединение к программе "Карта жителя"'
        from_email = form.cleaned_data['email']
        name_organization = form.cleaned_data['name_organization']
        inn_organization = form.cleaned_data['inn_organization']
        phone = form.cleaned_data['phone']
        user = form.cleaned_data['username']
        message = f'Название организации: {name_organization} ' \
                  f'ИНН организации: {inn_organization} ' \
                  f'Телефон: {phone} ' \
                  f'ФИО контактного лица: {user}'
        try:
            send_mail(f'{subject} от {from_email}', message,
                      DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL)
        except BadHeaderError:
            return HttpResponse('Ошибка в теме письма.')
        return redirect('success')


def success_view(request):
    return HttpResponse('Приняли! Спасибо за вашу заявку.')
