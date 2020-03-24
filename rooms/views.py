from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django_countries import countries
from django.core.paginator import Paginator
from . import models, forms

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


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):
        country = request.GET.get("country")
        if country:
            # 한번 검색했던것들을 웹이 기억하고 있게 하는 기능 = request.GET을 넣어준다
            form = forms.SearchForm(request.GET)
            # 만약 에러가 없다면 그 데이터 안에 뭐가 있는지 보는 기능
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                # 여기서부터는 field lookups를 이용하여 검색로직을 만들어보는 내용이다
                filter_args = {}

                # city로 검색
                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                # country로 검색
                filter_args["country"] = country

                # room_type으로 검색
                # foreignkey를 설정해 놓은 경우
                if room_type is not None:
                    filter_args["room_type"] = room_type

                # price로 검색
                # foreignkey를 설정해 놓은 경우
                if price is not None:
                    filter_args["price__lte"] = price

                # guest로 검색
                if guests is not None:
                    filter_args["guests__lte"] = guests

                # bedrooms로 검색
                if bedrooms is not None:
                    filter_args["bedrooms"] = bedrooms

                # beds로 검색
                if beds is not None:
                    filter_args["beds"] = beds

                # baths로 검색
                if baths is not None:
                    filter_args["baths__lte"] = baths

                # instant로 검색
                if instant_book is True:
                    filter_args["instant_book"] = True

                # superhost로 검색
                # foreignkey를 설정해 놓은 경우
                if superhost is True:
                    filter_args["host__superhost"] = True

                # amenities로 검색
                for amenity in amenities:
                    filter_args["amenities"] = amenity

                # facilities로 검색
                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})
