# uuid는 랜덤값을 불러오는 라이브러리다(이메일 인증할때 사용할 것임)
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# 가입할때 이메일 인증을 위한 send_email라이브러리
from django.core.mail import send_mail

from django.utils.html import strip_tags

from django.template.loader import render_to_string

# 일반 유저의 회원가입을 위한 창 생성
# 장고에 기본적으로 있는 AbstractUser 클래스를 상속받아 class를 만든다
class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "English"), (LANGUAGE_KOREAN, "Korean"))

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    # 데이터베이스의 초기값은 null=true를 하거나 defalut="" 를 써서 안에 디폴트값을 넣어줄수있다
    # 입력 필수값으로 지정하지 않으려면 blank=True를 해줘야한다
    # null과 blank는 데이터베이스이냐 필수입력값 지정이냐의 차이를 갖고 있다
    # uploads 폴더의 avatars 폴더에 avatar 관련 사진 파일들을 저장하겠다
    avatar = models.ImageField(upload_to="avatars", blank=True)
    # CharField는 한줄 작성, 글자수제한이 있음
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    # TextField는 여러 줄 작성 가능, 글자수 제한 없음
    bio = models.TextField(default="", blank=True)
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

    # 여기 유저네임은 이 클래스가 참조한 AbstractUser 클래스 안에 존재한다
    def __str__(self):
        return self.username
