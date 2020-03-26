from django.contrib import admin

# 기존에 장고에서 제공하는 UserAdmin을 불러온다
from django.contrib.auth.admin import UserAdmin

# from . import models 은 같은 폴더 내에 있는 models.py 파일을 불러온다는 뜻이다
from . import models

# 관리자의 회원관리를 위한 창 생성

# admin.site.register(models.User, CustomUserAdmin) 이거랑 밑에 @admin.register(models.User)랑 같은 뜻이다 장고문서 참고, 이거는 밑에 클래스 다음에 넣어서 적용한다
# user를 컨트롤 할 클래스가 CustomUserAdmin 이게 될거라는 것을 의미한다
# 이 @로 시작하는걸 Decorator라고 한다
# 클래스 위에쓰면 괄호 안에 있는 걸 클래스 안에 적용시켜준다
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    # 기존에 장고에서 제공하는 기능을 가져오고(UserAdmin.fieldsets) 추가로 내가 넣고싶은 기능(models.py에서 구현한 것)을 가져온다
    fieldsets = UserAdmin.fieldsets + (
        (
            "내가 추가하고 싶은것들",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
    )
