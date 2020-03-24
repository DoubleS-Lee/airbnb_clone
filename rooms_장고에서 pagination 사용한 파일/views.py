from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from . import models

# 우리는 Templates로(html) 우리가 원하는 값(파이썬에서 만든것)들을 보낼수있다
# 파이썬 문법을 render해서 html로 바꿔주는 역할을 한다

# 함수 이름은 core-urls.py에서 urlpattern에 정의한 이름과 같아야한다
def all_rooms(request):
    # 한 페이지당 보여지는 갯수 제한 및 다음 페이지로 넘기는 작업
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    # orphans를 넣으면 맨 끝에 해당 아이템 수보다 적게 남았을경우 이전페이지에서 출력하도록 한다
    # 마지막 페이지가 너무 비어보인다 싶으면 orphans를 이용해보자
    paginator = Paginator(room_list, 10, orphans=5)
    # 만약 사용자가 url을 아무렇게나 친다면?
    # 맨 첫번째 페이지로 redirect 시킨다
    # try, except를 사용
    try:
        rooms = paginator.page(int(page))
        # home.html 파일에 뒤에 내용을 넘겨준다는 뜻
        # html 파일의 이름은 templates 폴더에 있는 파일명과 같아야한다
        # 파일 경로를 지정한다 "rooms/home.html"
        return render(request, "rooms/home.html", {"page": rooms},)

    except EmptyPage:
        return redirect("/")

