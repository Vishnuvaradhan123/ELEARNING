from django.urls import path
from.import views

urlpatterns = [
    path('home/',views.store,name='store'),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/',views.updateItem, name="update_item"),
    path('register/', views.register,name="register"),
    path('login/',views.login,name="login"),
    path('home/',views.home,name="home"),
    path("forgot_password/",views.forgot_password,name="forgot_password"),
    path("send_otp",views.send_otp,name="send_otp"),
    path("reset_password/",views.reset_password,name="reset_password"),
    path("changed/",views.changed,name="changed"),
    path("logout/",views.logoutfunction,name="logout"),
]
