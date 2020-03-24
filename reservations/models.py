from django.db import models
from django.utils import timezone
from core import models as core_models


class Reservation(core_models.TimeStampedModel):

    """ Reservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"
    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    # 설정한 기간이 오늘과 비교했을때 이미 지났으면 False, 기간 중이면 True로 작용하게 하는 코드
    # 장고의 timezone을 import해와서 사용
    # from django.utils import timezone
    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    # 설정한 기간이 오늘과 비교했을때 지났으면 True
    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True
