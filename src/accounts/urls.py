from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('user/', views.userPage, name='user-page'),
    path('account/', views.accountSettings, name='account'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk>', views.customer, name='customer'),
    path('create_order/<str:pk>', views.create_order, name='create_order'),
    path('update_order/<str:pk>', views.update_order, name='update_order'),
    path('delete_order/<str:pk>', views.delete_order, name='delete_order'),
]

'''
1 - Submit email form                       //PasswordResetView.as_view()
2 - Email sent success message              //PasswordResetDoneView.as_view()
3 - Link to password reset form in Email    //PasswordResetConfirmView.as_view()
4 - Password successfully changed message   //PasswordResetCompleteView.as_view()
'''