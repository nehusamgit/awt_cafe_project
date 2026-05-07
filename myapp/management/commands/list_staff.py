from django.core.management.base import BaseCommand
from myapp.models import Staff

class Command(BaseCommand):
    help = 'List all staff users'

    def handle(self, *args, **options):
        staffs = Staff.objects.all()
        if not staffs:
            self.stdout.write(self.style.WARNING('No staff users found.'))
        else:
            for s in staffs:
                self.stdout.write(f"{s.id}: {s.username} / {s.password} (Name: {s.name})")
