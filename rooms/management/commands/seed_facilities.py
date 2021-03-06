from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):
    help = "This command creates facilities"

    #    def add_arguments(self, parser):
    #        parser.add_argument(
    #            "--times",
    #            help="How many times do you want me to tell you that I love you?",
    #        )

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]

        # 위에서 미리 준비해놓은 Amenities들을 object로 만들어서
        # 실제로 홈페이지에 연동시켜 Amenities 항목들을 다 채우는 방법
        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} facilities created!"))

        # 위의 코드를 작성한 뒤 TERMINAL 창에서
        # python manage.py seed_amenities를 입력해줘야한다

        # 이 방법을 사용하면 관리자페이지에서 일일히 입력해주지 않아도 한번에 일괄적으로 입력이 가능하다
