from django.contrib import admin
from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    """ Review Admin Definition """

    # models에서 만들어준 str을 admin에서 불러와서 쓸수도있다!
    # models에서 만들어준 평균 별점 기능을 불러왔다
    list_display = ("__str__", "rating_average")

