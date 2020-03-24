from django.db import models

# core를 새로 만들어줘서 다른 페이지들에 공통적으로 쓰이는 코드는 core에 모아준다
class TimeStampedModel(models.Model):

    # 작업했던 그 시간을 기록하기 위한 모델
    """ Time Stamped Model """
    # auto_now_add=True는 사용자가 model을 만들게 되면 장고가 자동으로 Model을 생성한 날짜와 시간을 기록해주는 서비스
    # auto_now=True는 업데이트 할때마다 이미 auto_now_add=True로 생성된 값을 새로고침하여 업데이트 해주는 기능
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # abstract 모델은 데이터베이스에 등록되지 않는다
        # 이걸 안해주면 데이터베이스의 이 모델이 등록이 되어 버린다
        abstract = True
