# 라이브러리 임포트 순서는 1.파이썬 기본 라이브러리 2.파이썬 외부 라이브러리 3.내가 만든 파이썬 라이브러리
# 순으로 하는 것이 보기 편하다
from django.utils import timezone
from django.db import models

from django.urls import reverse

# 장고 컨트리 import
from django_countries.fields import CountryField

# Time Stamped Model을 사용하기 위해 core.models를 불러옴
from core import models as core_models

# ForeignKey를 사용하기 위해 추가함
from users import models as user_models

from cal import Calendar


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Model Definition """

    class Meta:
        verbose_name = "Room Type"
        ordering = ["name"]


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    # uploads 폴더 안의 room_photos에 파일을 업로드 하겠다고 선언
    file = models.ImageField(upload_to="room_photos")
    # 여기서 원래 Room 클래스를 가져와야하는데
    # 파이썬은 상하수직방향으로 파일을 읽기때문에
    # 이 Photo 클래스를 Room 클래스의 밑으로 내리던가
    # ""를 이용해서 str화 해주는 방법을 사용해야한다
    # string화 해주면 파이썬은 이 값을 파이썬 내부에서 찾아서 적용해준다(정의 순서에 상관없이)
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()

    # django_countries를 설치 후(pipenv install django-countries)
    # config-setting.py로 가서 Third_party_apps에 "django_countries" 를 추가한다
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    # host(집주인)의 경우 기존에 만들어 놓은 users와 연동이 되는 시스템이기 때문에
    # ForeignKey를 사용한다
    # ForeignKey는 한 모델을 다른 모델과 연결시켜주기 위해 사용한다
    # ForeignKey는 일대다 모델(복수선택 불가)
    # on_delete=models.CASCADE  CASCADE는 폭포라는 뜻으로 제일 상위꺼가 지워지면 자연스레 그 밑에 속한것들도 다 지워진다는 뜻이다
    # 내가 만약 여기서 user를 삭제하면 자연스레 그 밑에 포함된 Room들도 다 지워진다
    # on_delete는 ForeignKey 만을 위한 것이다
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    # ManyToManyField는 ForeignKey와는 다르게 다대다 모델이다
    # 여러개의 모델을 다른 모델과 연결시켜주기 위해 사용(복수선택 가능)
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    # super 활용
    # city를 어떻게 작성하던지 첫번째 글자가 대문자가 되게 하는 코드
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    # view on site를 만든다
    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    # room에 대한 토탈 평점을 얻기 위한 함수 코드
    def total_rating(self):
        # all_reviews에 모든 리뷰 점수를 가져온다
        # reviews - model.py에 가보면 room이 related_name="reviews" 이렇게 reviews를 가지고 있다(room이 reviews를 가진다)
        # 따라서 여기서도 re
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0

    # 메인 화면에서 각 룸의 첫번째 사진 불러오기
    def first_photo(self):
        # 그냥 photo를 쓰면 사진 안의 QuerySet을 불러오고 photo,를 쓰면 이 array의 value를 불러온다
        # 여기서는 사진 즉 value를 불러와야하므로 photo,를 쓴다
        # 여기서 if문을 안썼을 경우 사진이 없다면 즉 len(self.photos.all()) == 0: 이라면
        # value가 없는데 value를 달라고 하는 경우가 되므로 에러가 발생한다
        # 여기서 None을 쓰거나 다른 정해진 사진으로 대체하면 된다
        if len(self.photos.all()) == 0:
            return None
        else:
            (photo,) = self.photos.all()[:1]
        return photo.file.url

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = this_month + 1
        if this_month == 12:
            next_month = 1
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(this_year, next_month)
        return [this_month_cal, next_month_cal]
