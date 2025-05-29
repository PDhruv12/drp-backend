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
    path('api/my-endpoint/', views.my_api_endpoint, name='my_endpoint'), 
    path('alive', views.alive, name='alive'),
    path('api/data/', views.example_data_view, name='example-data'),
    path('api/getdata/', views.get_data_from_db_orm, name='get-data'),
    path('event/<int:event_id>/', views.get_signups, name='get_signups'),
    path('event/<int:event_id>/signups/update/', views.update_signups, name='update_signups'),
    path('events/add/', views.add_events, name='add-data'),
]
