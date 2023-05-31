from django.urls import path, include

from . import views

app_name = 'tutor_me'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('', include("allauth.urls")),
    path('redirect/', views.view_redirect, name='redirect'),
    path('tutor/', views.tutor, name='tutor'),
    path('student/', views.student, name='student'),
    # path('tutor/availability/', views.save_availability, name='availability'),
    # path('tutor/availability/', views.available_times, name='availability_list'),
    path('student/schedule/submit_request',
         views.submit_request, name='submit_request'),
    path('student/schedule/success/', views.success, name='success'),
    ]
