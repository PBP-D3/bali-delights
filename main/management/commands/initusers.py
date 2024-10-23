from django.core.management import BaseCommand, call_command
from main.models import User

class Command(BaseCommand):
    help = "DEV COMMAND: Fill databasse with a set of data for testing purposes"

    def handle(self, *args, **options):
        call_command('loaddata','users')
        # Fix the passwords of fixtures
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()
            
# courtesy of: https://stackoverflow.com/questions/8017204/users-in-initial-data-fixture