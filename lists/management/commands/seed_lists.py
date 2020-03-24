import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.admin.utils import flatten
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models

name = "lists"

# 허수의 rooms들을 자동으로 생성하게 해주는 코드


class Command(BaseCommand):
    help = f"This command creates {name}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help=f"How many {name} do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        # 만약 .all()을 쓰기 싫다면 이렇게 하면 된다
        # rooms = room_models.Room.objects.all()[3:10]
        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(users),},
        )

        created = seeder.execute()
        # 이상한 모양 정리
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f"{number} {name} created!"))

        # 위의 코드를 작성한 뒤 TERMINAL 창에서
        # python manage.py seed_rooms --number 10 를 입력해줘야한다(10명을 만들고 싶은 경우)

        # 이 방법을 사용하면 관리자페이지에서 일일히 입력해주지 않아도 한번에 일괄적으로 입력이 가능하다
