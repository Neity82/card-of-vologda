from django.contrib import admin

from app_loyalty.models import News, Organization, Discount, Category


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Представление модели новостей в интерфейсе администратора"""
    list_display = ['created_up', 'title', 'get_description', 'is_active']
    list_display_links = ['title']
    list_editable = ['is_active']

    def get_description(self, obj):
        if len(obj.short_descr) > 150:
            description = obj.short_descr[:150] + '...'
        else:
            description = obj.short_descr
        return description

    get_description.short_description = 'краткое содержание'


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Представление организации в интерфейсе администратора"""
    list_display = ['name', 'inn', 'category', 'is_active']
    list_display_links = ['name']
    list_editable = ['is_active']
    list_filter = ['category']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Представление модели скидок в интерфейсе администратора"""
    list_display = ['organization', 'description', 'is_active']
    list_display_links = ['organization']
    list_editable = ['is_active']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Представление модели категорий в интерфейсе администратора"""
    list_display = ['name']
