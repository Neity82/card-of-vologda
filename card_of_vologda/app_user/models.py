from django.db.models import QuerySet
from softdelete.models import SoftDeleteObject

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from app_loyalty.models import Organization
from app_user.manager import CustomUserManager

TYPE_CHOICE = {
    ('Списано', 'Списано'),
    ('Начислено', 'Начислено')
}


class CustomUser(SoftDeleteObject, AbstractUser):
    """Модель пользователя/покупателя"""

    phone_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$",
                                 message='Не допустимый формат')
    card_regex = RegexValidator(regex=r"^2200\d{12}$",
                                message='Карта содержит не 16 цифр или не платежной системы Мир')

    username = None

    email = models.EmailField(
        verbose_name='email',
        unique=True
    )

    middle_name = models.CharField(
        max_length=50,
        verbose_name='отчество',
        blank=True
    )

    phone = models.CharField(
        verbose_name='телефон',
        validators=[phone_regex],
        max_length=16,
        blank=True
    )

    num_card = models.CharField(
        verbose_name='номер карты жителя',
        validators=[card_regex],
        max_length=16,
        blank=True
    )

    balance = models.PositiveIntegerField(
        verbose_name='баланс',
        default=0
    )

    is_organization = models.BooleanField(
        verbose_name='представитель организации',
        default=False
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name='организация',
        related_name='user',
        blank=True,
        null=True
    )

    can_deduct = models.BooleanField(
        verbose_name='может списывать',
        default=False
    )

    can_accrue = models.BooleanField(
        verbose_name='может начислять',
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self) -> str:
        """Метод возвращает строковое представление объекта"""

        return f'{self.last_name} {self.first_name} {self.middle_name}'


class History(SoftDeleteObject, models.Model):
    """Модель истории начисления и списания бонусов пользователя"""

    created_up = models.DateField(
        verbose_name='дата',
        auto_now_add=True
    )

    type = models.CharField(
        max_length=100,
        verbose_name='тип операции',
        choices=TYPE_CHOICE
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        related_name='history'
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name='организация',
        related_name='history'
    )

    sum_points = models.PositiveIntegerField(
        verbose_name='количество баллов'
    )

    class Meta:
        db_table = 'history'
        verbose_name = 'история'
        verbose_name_plural = 'истории'
        ordering = ['-created_up']

    def __str__(self) -> str:
        """Метод возвращает строковое представление объекта"""
        return f'{self.created_up} {self.type}'

    @classmethod
    def get_history_list(cls, user: CustomUser) -> QuerySet['History']:
        """
        Получение списка истории начисление и списания бонусов

        :param user: Пользователь
        :type user: CustomUser
        :return: Список истории
        :type:QuerySet['History']
        """
        result: QuerySet['History'] = cls.objects.filter(user=user)
        return result
