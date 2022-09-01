"""thscoreboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

import logging

from django.contrib import admin
from django.urls import include, re_path, path
from replays import views
from thscoreboard import settings

urlpatterns = [
    path('users/', include('users.urls')),
    path('', views.index),
    path('replays/', include('replays.urls')),
    path('admin/', admin.site.urls),
]

# Install django-rosetta if (and only if) it is listed as an installed app.
# This should not be the case in prod.
if 'rosetta' in settings.INSTALLED_APPS:
    logging.info('Including django-rosetta at /rosetta')
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]
