from django.core.management import BaseCommand
from faker import Faker

from core.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()
        for _ in range(30):
            Product.objects.create(
                title=faker.company() + " " + faker.word(),
                description=faker.text(100),
                image=faker.image_url(),
                price=faker.random_number(digits=2)
            )
