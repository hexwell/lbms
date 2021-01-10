from django.contrib.auth.models import User, Permission, Group as PermissionGroup
from django.core.management import BaseCommand

from lbms_app.models import Group as LbmsGroup

PERMISSION_GROUP_NAME = 'Users'

ETTORE_LBMS_GROUP_NAME = 'Ettore'
FAMILY_LBMS_GROUP_NAME = 'Famiglia'


def _apply_superuser_permissions():
    user = User.objects.filter(is_superuser=True).first()

    user.user_permissions.set(Permission.objects.all())

    user.save()


def _apply_permission_group():
    group = PermissionGroup.objects.filter(name=PERMISSION_GROUP_NAME)

    if group:
        group = group.first()

    else:
        group = PermissionGroup(name=PERMISSION_GROUP_NAME)
        group.save()

    for user in User.objects.all():
        user.groups.add(group)


class Command(BaseCommand):
    help = f'Initialize LBMS'

    def __apply_group(self):
        pass

    def handle(self, *args, **options):
        _apply_superuser_permissions()
        _apply_permission_group()

        ettore_group = LbmsGroup.objects.filter(name=ETTORE_LBMS_GROUP_NAME)
        family_group = LbmsGroup.objects.filter(name=FAMILY_LBMS_GROUP_NAME)

        if not (ettore_group and family_group):
            LbmsGroup(name=ETTORE_LBMS_GROUP_NAME).save()
            LbmsGroup(name=FAMILY_LBMS_GROUP_NAME).save()
