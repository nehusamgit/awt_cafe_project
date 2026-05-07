from django.db import migrations


def create_default_staff(apps, schema_editor):
    Staff = apps.get_model('myapp', 'Staff')
    default_staff = [
        {'name': 'John Staff', 'email': 'john@example.com', 'username': 'john_staff', 'password': 'staff123'},
        {'name': 'Jane Staff', 'email': 'jane@example.com', 'username': 'jane_staff', 'password': 'staff456'},
        {'name': 'Mike Staff', 'email': 'mike@example.com', 'username': 'mike_staff', 'password': 'staff789'},
    ]
    for staff_data in default_staff:
        Staff.objects.get_or_create(username=staff_data['username'], defaults=staff_data)


def delete_default_staff(apps, schema_editor):
    Staff = apps.get_model('myapp', 'Staff')
    usernames = ['john_staff', 'jane_staff', 'mike_staff']
    Staff.objects.filter(username__in=usernames).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_default_staff, reverse_code=delete_default_staff),
    ]
