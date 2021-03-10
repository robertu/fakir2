"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from fakir import views
from django.contrib.auth.views import LogoutView
from django.conf import settings

app_name = 'fakir'

urlpatterns = [
    path('', views.index, name='index'),
	path('', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path(
    'logout/',
    LogoutView.as_view(template_name=settings.LOGOUT_REDIRECT_URL),
    name='logout'
    ),
	    path('manage/', views.manage, name='manage'),
]
