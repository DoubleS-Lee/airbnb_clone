from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
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
    paginate_by = 12
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


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
    # fields에 Edit Room에서 수정하고 싶은 것들을 정의해준다
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    # 유저가 다른 사람의 room을 edit 하러 갔을 경우 에러를 띄우는 함수
    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):
    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Cant delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated!"
    fields = ("caption",)

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):
    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):
    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        # many-to-many를 저장하기 위해서 사용한다(Amenities, Facilities, HouseRules 정보를 저장하기 위함)
        form.save_m2m()
        messages.success(self.request, "Room Uploaded")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
