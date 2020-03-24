import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations import models as reservation_models
from users import models as user_models
from rooms import models as room_models

name = "reservations"

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
            reservation_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25)),
            },
        )

        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {name} created!"))

        # 위의 코드를 작성한 뒤 TERMINAL 창에서
        # python manage.py seed_rooms --number 10 를 입력해줘야한다(10명을 만들고 싶은 경우)

        # 이 방법을 사용하면 관리자페이지에서 일일히 입력해주지 않아도 한번에 일괄적으로 입력이 가능하다
