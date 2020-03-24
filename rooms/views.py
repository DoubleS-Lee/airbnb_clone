from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models

# 우리는 Templates로(html) 우리가 원하는 값(파이썬에서 만든것)들을 보낼수있다
# 파이썬 문법을 render해서 html로 바꿔주는 역할을 한다

# 여기서 불러온 함수인 ListView는 우리가 models.Room을 list up 해야한다는걸 기본적으로
# 알고 적용해주고 있다
# 즉 별도의 프로그래밍이 필요가 없다
# ccbv.co.uk 에 가면 상세설정에 대한 설명이 나와있다
class HomeView(ListView):

    """ HomeView Definition """

    # ccbv.co.uk 에 가면 상세설정에 대한 설명이 나와있다
    # 컨텐츠 불러오기
    model = models.Room
    # 페이지 당 콘텐츠 개수
    paginate_by = 10
    # 초기 자동 정렬방식
    ordering = "created"
    # 마지막 페이지 뷰에 대한 설정
    paginate_orphans = 5

    context_object_name = "rooms"


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


def search(request):
    # 기본 값 설정하는 코드
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    # 기본 값 설정하는 코드
    country = request.GET.get("country", "KR")
    # search.html에서 pk는 int 이므로 여기서 int를 써준다
    room_type = int(request.GET.get("room_type", "0"))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    # 선택된(selected) amenity와 Facility들을 알아내기 위한 코드
    # amenity와 Facility가 개수가 여러개이므로 getlist를 사용한다
    # 이렇게 해서 list로 불러온다
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    # 기본 값 모음
    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    # 데이터 베이스 내의 값 모음
    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    # 여기서부터는 field lookups를 이용하여 검색로직을 만들어보는 내용이다
    filter_args = {}

    # city로 검색
    if city != "Anywhere":
        filter_args["city__startswith"] = city

    # country로 검색
    filter_args["country"] = country

    # room_type으로 검색
    # foreignkey를 설정해 놓은 경우
    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    # price로 검색
    # foreignkey를 설정해 놓은 경우
    if price != 0:
        filter_args["price__lte"] = price

    # guest로 검색
    if guests != 0:
        filter_args["guests__lte"] = guests

    # bedrooms로 검색
    if bedrooms != 0:
        filter_args["bedrooms"] = bedrooms

    # beds로 검색
    if beds != 0:
        filter_args["beds"] = beds

    # baths로 검색
    if baths != 0:
        filter_args["baths__lte"] = baths

    # instant로 검색
    if instant is True:
        filter_args["instant_book"] = True

    # superhost로 검색
    # foreignkey를 설정해 놓은 경우
    if superhost is True:
        filter_args["host__superhost"] = True

    # amenities로 검색
    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    # facilities로 검색
    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    rooms = models.Room.objects.filter(**filter_args)

    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})
