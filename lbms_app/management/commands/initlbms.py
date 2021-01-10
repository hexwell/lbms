from django.contrib.auth.models import Permission, Group as PermissionGroup, User
from django.core.management import BaseCommand

from lbms_app.models import Group as LbmsGroup, UserGroup

ETTORE_LBMS_GROUP_NAME = 'Ettore'
FAMILY_LBMS_GROUP_NAME = 'Famiglia'

PERMISSION_GROUP_NAME = 'Users'


def _init_lbms_groups():
    ettore_group = LbmsGroup.objects.filter(name=ETTORE_LBMS_GROUP_NAME)
    family_group = LbmsGroup.objects.filter(name=FAMILY_LBMS_GROUP_NAME)

    if not (ettore_group and family_group):
        LbmsGroup(name=ETTORE_LBMS_GROUP_NAME).save()
        LbmsGroup(name=FAMILY_LBMS_GROUP_NAME).save()


def _init_superuser():
    user = User.objects.filter(is_superuser=True).first()

    for group in LbmsGroup.objects.all():
        UserGroup(user=user, group=group).save()

    user.user_permissions.set(Permission.objects.all())

    user.save()


def _init_permission_group():
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

    def handle(self, *args, **options):
        _init_lbms_groups()
        _init_superuser()
        _init_permission_group()
