from typing import List

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.db.models import QuerySet

from app_user.models import CustomUser, History


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Представление модели пользователя в интерфейсе администратора"""

    form = UserChangeForm
    add_form = UserCreationForm
    save_on_top = True

    list_display = ['id', 'last_name', 'first_name', 'middle_name', 'email',
                    'get_groups', 'organization', 'can_deduct', 'can_accrue']
    list_display_links = ['id', 'last_name']
    list_editable = ['can_deduct', 'can_accrue']

    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_organization', 'organization', 'can_deduct', 'can_accrue')}),
        ('Персональная информация', {
            'fields': ('last_name', 'first_name', 'middle_name', 'phone', 'num_card', 'balance')
        }),
        ('Права доступа', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined',)
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'is_organization', 'password1', 'password2')}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)

    def get_groups(self, obj: CustomUser) -> str:
        """
        Получаем перечень групп, в которые входит пользователь

        :param obj: Пользователь
        :type obj: CustomUser
        :return: Перечень групп
        :rtype: str
        """

        groups: QuerySet['Groups'] = obj.groups.all()
        groups_list: List[str] = []
        if groups:
            for i in groups:
                groups_list.append(str(i))
            groups_str = ', '.join(groups_list)
            return groups_str

    get_groups.short_description = 'группа'


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    """Представление модели истории пользователя в интерфейсе администратора"""

    list_display = ['created_up', 'type', 'user', 'organization', 'sum_points']
    list_display_links = ['created_up']

