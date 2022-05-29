from django import template


register = template.Library()


@register.simple_tag
def get_normalize_card(card: int) -> str:
    """
    Преобразование номера карты в строку в формате:
    XXXX XXXX XXXX XXXX

    :param card: Номер карты
    :type card: int
    :return: Преобразованный номер карты
    :rtype: str
    """
    card = str(card)
    return f'{card[:4]} {card[4:8]} {card[8:12]} {card[12:16]}'


