from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# rooms의 models.py의 RoomType, Facility, Amenity, HouseRule 클래스를 참조한다 는 뜻
@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    # 최상단에 리스트를 만들어주고(Room Types, Facilities, Amenities, House Rules 모두에게 해당됨)
    list_display = ("name", "used_by")

    # 설정된 값의 수를 세어서 보여준다(Room Types, Facilities, Amenities, House Rules 모두에게 해당됨)
    def used_by(self, obj):
        return obj.rooms.count()


# Admin 안에 다른 Admin을 넣는 방법
# rooms 안에 photo를 넣기 위한 방법
class PhotoInline(admin.TabularInline):
    model = models.Photo


# rooms의 models.py의 Room 클래스를 참조한다 는 뜻
@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition"""

    # 이 class 안에 PhotoInline Admin을 넣는다
    # rooms 안에 photo를 넣기 위한 방법
    inlines = (PhotoInline,)

    # 정보 작성을 할때 카테고리화 하여 나눠주는 역할
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")},),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")},),
        (
            "More About the Space",
            {
                # classes collapse를 넣으면 축소하기 확대하기 기능을 추가할 수 있다
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("Last Details", {"fields": ("host",)},),
    )

    # 최상단에 정렬을 할 수 있는 인덱스행을 만들어준다
    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        # count_amenities 처럼 함수로 만든 display를 사용하면 웹상에서 클릭이 안된다
        # 밑에 만들어놓은 함수가 있다
        "count_amenities",
        "count_photos",
        # 이건 rooms-models.py에 있는 total_rating 함수를 불러온거다
        # 이 클래스 상단에 @admin.register(models.Room) 이렇게 models.Room을 참조했기에 가능함
        "total_rating",
    )

    # 처음 불러오자마자 기본으로 적용되어있는 정렬방식 지정 =로딩후 즉시 정렬
    # 작성하는 순서대로 정렬이 된다
    ordering = ("name", "price", "bedrooms")

    # 필터를 칠 수 있는 시스템을 만들어준다
    list_filter = (
        "instant_book",
        # host 안에 있는 superhost와 gender의 정보를 가져와서 필터를 만들고 싶은 경우 사용 방법
        # 이때 host는 rooms-models.py 안에 Room 클래스 안에 있으며, users.User를 참조하고 있기때문에
        # users-models.py에 가면 User 클래스가 있는데 여기에 있는 superhost와 gender를 불러오는 것이다
        "host__superhost",
        "host__gender",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    # 여러가지 항목을 선택하는 메뉴를 만들때 사용
    # manytomany Relationship 에서 작동한다
    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    # 유저가 엄청 많아질경우 모든 유저를 한번에 표현하기에는 벅차다
    # 그래서 표기는 아이디 값으로 해주고 상세 정보를 보려면 옆에 메뉴를 클릭하게 하는게 좋다
    raw_id_fields = ("host",)

    # 검색기능추가
    # 장고 Docu로 가서 admin 그리고 search로 검색하고 살펴보면 추가 정보들이 있다
    # host의 username을 가지고 검색을 하고 싶을때 사용하는 방법
    search_fields = ("=city", "^host__username")

    # 룸 어매니티의 갯수를 세어서 list에 집어넣고 싶은 경우 사용
    # 이 함수안에 count_amenities는 self(=RoomAdmin 클래스)를 받고, 그 뒤 obj를 받는다(현재 rooms 안의 row(홈페이지 상))
    def count_amenities(self, obj):
        return obj.amenities.count()

    # 등록된 사진의 갯수를 세어서 list에 집어넣고 싶은 경우 사용
    # models.py에서 Photo 클래스 안 room에 related_name에 photos를 연동해줬기 때문에
    # 여기서 obj가 photos를 가지게 된다
    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"

    # list_display 상 count_amenities 함수의 이름을 바꾸고 싶은 경우 사용
    # count_amenities.sort_description = "Hello Sexy"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    # 썸네일에 사진을 나오게 하기
    # mark_safe가 없으면 주소만 나오게 된다
    # 장고에게 이건 안전해 라는 신호를 줘야하는데 그게 mark_safe다
    # mark_safe를 불러오려면 from django.utils.html import mark_safe 를 import 해야한다
    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"

