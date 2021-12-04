from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="home"),
    path('login',views.login_view,name="login"),
    path('register',views.register_view,name="register"),
    path('logout',views.logout_view,name="logout"),
    path('search',views.search,name="search"),
    path('detail/<int:id>',views.detail,name="detail"),
    path('otp',views.otp,name="otp"),
    path('payment/<int:id>',views.payment,name="payment"),
    path('success',views.success,name="success"),
    path('about',views.about,name="about"),
    path('account',views.account,name="account"),
    path('delete/<int:id>',views.delete,name="delete"),
    path('alert',views.alert,name="alert"),
    path('alertdelete/<int:id>',views.alertdelete,name="alertdelete"),
]
