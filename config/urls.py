"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include

# settings.py를 불러온다
from django.conf import settings

from django.conf.urls.static import static


# 여기서 "admin/"은 url이고, admin.site.urls는 view이다
urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("rooms/", include("rooms.urls", namespace="rooms")),
    path("users/", include("users.urls", namespace="users")),
    path("admin/", admin.site.urls),
]

# 미디어 파일을 가르키는 폴더의 경로 설정은 개발환경에서만 돌아가게 만들어놨다
# 실제로 아마존이나 서버에 올릴때는 이 경로는 사용하지 않을 예정 이어서 if 문을 만듦
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
