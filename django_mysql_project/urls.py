"""django_mysql_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path, include
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('payhistory.urls')),
# ]

from django.urls import path, include
from django.contrib import admin
from django.conf.urls import url
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi


schema_url_v1_patterns = [
    url('api/', include('payhistory.urls')),
    url('api/', include('user.urls')),
]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="pay history API",
        default_version='v1',
        description="API 문서"
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_v1_patterns,
)

urlpatterns = [
    url('admin/', admin.site.urls),
    url('api/', include('payhistory.urls')),
    url('api/', include('user.urls')),

    # Auto DRF API docs
    url(r'^swagger(?P<format>\.json|\.yaml)/v1$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/v1/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/v1/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
]
