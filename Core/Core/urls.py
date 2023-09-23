"""
URL configuration for Core project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Руководство пользователя',
        default_version='v1',
        description='Инструкция по использованию рест ресурса(ну как с пылесосом, тоже читать никто не будет',
    ),
    public=True,

)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('Services.urls.auth')),
    path('profile/', include('Services.urls.profile')),
    path('moderation/', include('Services.urls.moderation')),
    path('', include('Services.urls.mainpage')),
    path('api/', include('api.router.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0))

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
