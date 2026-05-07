from django.core.management.base import BaseCommand
from myapp.models import Staff

class Command(BaseCommand):
    help = 'Initialize staff members'

    def handle(self, *args, **options):
        staff_data = [
            ('John Staff', 'john@example.com', 'john_staff', 'staff123'),
            ('Jane Staff', 'jane@example.com', 'jane_staff', 'staff456'),
            ('Mike Staff', 'mike@example.com', 'mike_staff', 'staff789'),
        ]

        for name, email, uname, pword in staff_data:
            staff, created = Staff.objects.get_or_create(
                username=uname,
                defaults={'name': name, 'email': email, 'password': pword}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created staff: {uname}'))
            else:
                staff.password = pword  # Ensure password matches
                staff.save()
                self.stdout.write(self.style.WARNING(f'Staff {uname} already exists, updated password'))
