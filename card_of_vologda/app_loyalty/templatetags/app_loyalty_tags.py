from typing import Dict, Union

from django import template
from django.db.models import QuerySet

from app_loyalty.models import Category

register = template.Library()


# @register.simple_tag(name='get_cats')
# def get_categories(filter_value=None) -> QuerySet[Category]:
#     """
#     Получаем список категорий
#
#     :param filter_value:
#     :return:
#     """
#     if not filter_value:
#         return Category.objects.all()
#     else:
#         return Category.objects.filter(pk=filter_value)


@register.inclusion_tag('app_loyalty/inc/_categories.html')
def show_categories(sort=None,
                    cat_selected: int = 0
                    ) -> Dict[str, Union[QuerySet[Category], int]]:
    """
    Получаем список категорий и параметр selected

    :param sort:
    :param cat_selected: индекс selected
    :type: int
    :return: Список категорий и параметр selected
    :rtype: Dict[str, Union[QuerySet[Category], int]]
    """
    if not sort:
        cats: QuerySet[Category] = Category.objects.all()
    else:
        cats: QuerySet[Category] = Category.objects.order_by(sort)

    return {'categories': cats, 'cat_selected': cat_selected}
