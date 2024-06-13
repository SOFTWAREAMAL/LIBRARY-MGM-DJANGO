"""
URL configuration for django_library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from library_mgm import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',views.admin_login),
    path('',views.login),
    path('login',views.login),
   # path('al_message',views.al_message),
    path('homepage',views.homepage),
    
    path('view',views.view_book_details),
    path('view_student_record',views.view_student_record),
    
    path('check_book_availability',views.check_book_availability),
    path('add_book', views.add_book),
    path('issue_book',views.issue_book),
    path('return_book',views.return_book),
    path('fine',views.fine),
    
    path('logout',views.logout),
   
]
