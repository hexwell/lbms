from django.contrib.auth.models import User, Permission, Group
from django.core.management import BaseCommand

GROUP_NAME = 'Users'


def _apply_superuser_permissions():
    user = User.objects.filter(is_superuser=True).first()

    user.user_permissions.set(Permission.objects.all())

    user.save()


def _apply_group():
    group = Group.objects.filter(name=GROUP_NAME)

    if group:
        group = group.first()

    else:
        group = Group(name=GROUP_NAME)
        group.save()

    for user in User.objects.all():
        user.groups.add(group)


class Command(BaseCommand):
    help = f'Apply all permissions to superuser, create {GROUP_NAME} group and assign it to all users.'

    def __apply_group(self):
        pass

    def handle(self, *args, **options):
        _apply_superuser_permissions()
        _apply_group()
