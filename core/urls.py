from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name="home"),
    path('add_news', views.add_news, name="add_news"),
    path('login', views.login, name="login"),
    path('sign-up', views.signup, name="sign-up"),
    path('choose', views.choose, name="choose"),
    path('semilleros', views.semilleros, name="semilleros"),
    path('estadisticas', views.estadisticas, name="estadisticas"),
    path(r'news/<int:id_item>', views.news, name="news")
]
