from typing import List

from django.core.validators import RegexValidator
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from softdelete.models import SoftDeleteObject


def news_img_directory_path(instance, filename):
    """Функция формирует путь для размещения изображения новости"""
    return 'news_img/{id}/{filename}'.format(id=instance.id, filename=filename)


class Category(SoftDeleteObject, models.Model):
    """Модель категории"""

    name = models.CharField(
        max_length=150,
        verbose_name='категория'
    )

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        """Генерирует ссылку для детального просмотра новости"""
        return reverse('category', kwargs={'pk': self.pk})


class Organization(SoftDeleteObject, models.Model):
    """Модель органицации-партнера, которая предоставляет скидку"""

    inn_regex = RegexValidator(
        regex=r"^\d{10,12}$",
        message='ИНН может содержать 10 или 12 цифр.'
    )

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    inn = models.PositiveIntegerField(
        verbose_name='ИНН',
        validators=[inn_regex]
    )

    website = models.EmailField(
        verbose_name='сайт организации',
        blank=True
    )

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        verbose_name='категория',
        related_name='organization'
    )

    is_active = models.BooleanField(
        verbose_name='активна',
        default=True
    )

    class Meta:
        db_table = 'organizations'
        verbose_name = 'организация'
        verbose_name_plural = 'организации'

    def __str__(self):
        """Метод возвращает строковое представление объекта"""
        return f'{self.name} (ИНН {self.inn})'


class News(SoftDeleteObject, models.Model):
    """Модель новости"""

    title = models.CharField(
        max_length=250,
        verbose_name='заголовок'
    )

    short_descr = models.TextField(
        verbose_name='краткое содержание'
    )

    description = models.TextField(
        verbose_name='содержание'
    )

    created_up = models.DateField(
        verbose_name='дата публикации',
        auto_now_add=True
    )

    img = models.ImageField(
        verbose_name='изображение',
        blank=True,
        upload_to=news_img_directory_path
    )

    is_active = models.BooleanField(
        verbose_name='активна',
        default=True
    )

    class Meta:
        db_table = 'news'
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
        ordering = ['-created_up']

    def __str__(self) -> str:
        """Метод возвращает строковое представление объекта"""
        return self.title

    def get_absolute_url(self):
        """Генерирует ссылку для детального просмотра новости"""
        return reverse('news_detail', kwargs={'pk': self.pk})

    @classmethod
    def get_news_list(cls, limit: int = None) -> List['News']:
        """
        Метод получения списка активных новостей в размере limit

        :param limit: количество новостей в списке
        :type limit: int
        :return: список новостей
        :rtype: List[News]
        """

        result: List['News'] = cls.objects.filter(is_active=True)
        return result[:limit]


class Discount(SoftDeleteObject, models.Model):
    """Модель скидки"""

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE,
        verbose_name='организация',
        related_name='discount'
    )

    description = models.TextField(
        verbose_name='описание'
    )

    created_up = models.DateField(
        verbose_name='дата добавления',
        auto_now_add=True
    )

    is_active = models.BooleanField(
        verbose_name='активна',
        default=True
    )

    class Meta:
        db_table = 'discounts'
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'
        ordering = ['-created_up']

    def __str__(self) -> str:
        """Метод возвращает строковое представление объекта"""
        return self.organization.name

    @classmethod
    def get_discount_list(cls,
                          category_id: int = None,
                          limit: int = None
                          ) -> List['Discount']:
        """
        Метод получения списка активных скидок в размере limit

        :param category_id: id категории
        :type category_id: int
        :param limit: количество скидок в списке
        :type limit: int
        :return: список скидок
        :rtype: List[Discount]
        """
        if category_id:
            result: List['Discount'] = cls.objects.filter(
                is_active=True,
                organization__category_id=category_id
            )
        else:
            result: List['Discount'] = cls.objects.filter(is_active=True)
        return result[:limit]
