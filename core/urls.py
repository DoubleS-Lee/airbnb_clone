from django.urls import path
from rooms import views as room_views

# config.urls 안의 path("", include("core.urls", namespace="core")) 이거를 동작하게 하기 위해서는
# app_name을 반드시 지정해줘야한다 여기서의 app_name은 namespace와 같은것이어야한다(여기서는 core 임)
app_name = "core"

# urls.py를 만들때 urlpatterns는 필수로 작성해야한다
# 여기서 ""는 /를 의미한다
urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]
