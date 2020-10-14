from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login',views.login),
    path('success',views.success),
    path('logout',views.logout),
    path('post',views.post),
    path('comment',views.comment),
    path('delete/<int:message_id>/<int:user_id>',views.delete)
]