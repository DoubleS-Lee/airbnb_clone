# uuid는 랜덤값을 불러오는 라이브러리다(이메일 인증할때 사용할 것임)
import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# 가입할때 이메일 인증을 위한 send_email라이브러리
from django.core.mail import send_mail

from django.utils.html import strip_tags

from django.shortcuts import reverse

from django.template.loader import render_to_string

from core import managers as core_managers

# 일반 유저의 회원가입을 위한 창 생성
# 장고에 기본적으로 있는 AbstractUser 클래스를 상속받아 class를 만든다
class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
        (GENDER_OTHER, _("Other")),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, _("English")),
        (LANGUAGE_KOREAN, _("Korean")),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    # 데이터베이스의 초기값은 null=true를 하거나 defalut="" 를 써서 안에 디폴트값을 넣어줄수있다
    # 입력 필수값으로 지정하지 않으려면 blank=True를 해줘야한다
    # null과 blank는 데이터베이스이냐 필수입력값 지정이냐의 차이를 갖고 있다
    # uploads 폴더의 avatars 폴더에 avatar 관련 사진 파일들을 저장하겠다
    # 번역을 위해서 _("gender")를 작성하였다
    avatar = models.ImageField(_("avatar"), upload_to="avatars", blank=True)
    # CharField는 한줄 작성, 글자수제한이 있음
    gender = models.CharField(
        _("gender"), choices=GENDER_CHOICES, max_length=10, blank=True
    )
    # TextField는 여러 줄 작성 가능, 글자수 제한 없음
    bio = models.TextField(_("bio"), default="", blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )

    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="", blank=True)
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )
    objects = core_managers.CustomModelManager()

    # 이건 user의 profile로 가게하는 url을 만들어주는 과정에서 작성한 함수이다
    # 이렇게 url을 작성한다면 admin 패널에서도 해당 메뉴가 표시되어서 관리가 가능해진다
    # get_absolute_url을 공부해보자
    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )
            send_mail(
                "Verify Airbnb Account",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return
