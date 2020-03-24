import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models

# 허수의 rooms들을 자동으로 생성하게 해주는 코드


class Command(BaseCommand):
    help = "This command creates many rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many users do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        # 생성해놓은 users 정보를 가져오는 코드
        # room을 생성하려면 host가 반드시 있어야하기 때문에 user와 room을 매칭시켜주는 작업이 필요하다
        # 같은 원리로 room_types도 반드시 있어야한다
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        # 기본 add_entity에 room 안에 random으로 user를 집어넣는 람다함수를 만든다
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(0, 999999),
                "guests": lambda x: random.randint(1, 20),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        created_photos = seeder.execute()
        # 이상한 모양 정리
        created_clean = flatten(list(created_photos.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        for pk in created_clean:
            # 생성된 모든 room을 Primary key로 그 room을 찾고
            # room의 instance를 받기 위함
            room = room_models.Room.objects.get(pk=pk)

            # 최소 3, 최대 10이나 17까지 사진을 만들고
            for i in range(3, random.randint(10, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    # 생성된 room에게 파일을 준다
                    file=f"room_photos/{random.randint(1,31)}.webp",
                )

            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)

            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)

            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))

        # 위의 코드를 작성한 뒤 TERMINAL 창에서
        # python manage.py seed_rooms --number 10 를 입력해줘야한다(10명을 만들고 싶은 경우)

        # 이 방법을 사용하면 관리자페이지에서 일일히 입력해주지 않아도 한번에 일괄적으로 입력이 가능하다
