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
    path('<user_id>/event/create', views.add_event, name='add_event'),
    path('<user_id>/community/add/', views.add_community, name='add-community'),
    path('<user_id>/my-communities/', views.get_my_communities, name='my-communities'),
    path('<user_id>/communities/all/', views.get_communities, name='communities'),
    path('<user_id>/community/messages/get', views.get_messages, name='community messages'),
    path('<user_id>/community/message/send', views.send_message, name='send message'),

    path('user-login/', views.login, name="logins user"),
    path('user-create/', views.add_user, name='adds user'),
    path('user-view', views.users, name='users'),
    
    path('delete-all/', views.delete_all_events, name='delete-all'),
    path('delete/<int:event_id>/', views.delete_particular_event),
    path('images-view', views.view_images),
    path('tags', views.getTags),
    path('<user_id>/event-all/', views.get_events_all, name='all events'),
    path('add/<user_id>/<name>/<description>', views.add_community_from_browser),
    path('addmember/<user_id>/<community_id>', views.make_member),
    path('delete/community/<community_id>', views.delete_community),
]
