from django.core.management.base import BaseCommand
from patients.models import CustomUser

class Command(BaseCommand):
    help = 'Create a superuser with specified email and password'

    def handle(self, *args, **kwargs):
        email = 'admin@example.com'
        password = 'admin'

        user = CustomUser.objects.create(
            email=email,
            is_staff=True,
            is_superuser=True
        )
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Superuser "{email}" has been successfully created.'))
