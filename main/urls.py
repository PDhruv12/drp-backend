"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import core.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<user_id>/events/', views.get_events, name='events'), # List of events for each user
    path('<user_id>/event/<int:event_id>/', views.get_event, name='event_specific'),
    path('<user_id>/event/<int:event_id>/signup/', views.event_sign_up, name='signup'),
    path('<user_id>/event/create/', views.add_event, name='add_event'),
    
    path('user', views.add_user, name='adds user'),
    path('user-view', views.users, name='users'),
    path('delete-all/', views.delete_all_events, name='delete-all'),
]
