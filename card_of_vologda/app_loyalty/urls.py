from django.urls import path

from app_loyalty.views import Home, NewsDetail, NewsList, DiscountList, \
    DiscountCategory, about_project, Application, success_view

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('news/', NewsList.as_view(), name='news'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('discount/', DiscountList.as_view(), name='discount'),
    path('category/<int:pk>/', DiscountCategory.as_view(), name='category'),
    path('about_project/', about_project, name='about'),
    path('application/', Application.as_view(), name='application'),
    path('success/', success_view, name='success'),
]
