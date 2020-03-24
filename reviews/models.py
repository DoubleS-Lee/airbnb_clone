from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField()
    accuracy = models.IntegerField()
    communucation = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    Value = models.IntegerField()
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    # 표시하길 원하는 정보를 경로를 이용해서 표시하기
    # 또한 이런것도 가능하다
    # 위에서 ForeignKey를 정의했으면 그 클래스안에 들어가서 거기에 있는 값을 return 값으로 넣을 수도 있다
    # return self.room.country 이런식으로도 가능하다는 뜻이다
    # ForeignKey만 설정되어있으면 클래스의 클래스의 클래스의 클래스 안의 값
    # 이런식으로 계속 타고 들어가서 설정해줄수도 있다
    def __str__(self):
        return f"{self.review} - {self.room}"

    # 리뷰의 별점을 평균내는 기능
    # 이 함수를 admin에서 만들지 않고 여기 models에서 만든 이유 :
    # 별점 기능을 admin 뿐만 아니라 프론트 엔드나 기타 다른 곳에서도 사용하기 위해서
    def rating_average(self):
        avg = (
            self.accuracy
            + self.communucation
            + self.cleanliness
            + self.location
            + self.check_in
            + self.Value
        ) / 6
        return round(avg, 2)

    # rating_average가 list_display에 표시되는 이름 바꾸기
    rating_average.short_description = "Avg."

