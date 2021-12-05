from getpass import getpass

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group as PermissionsGroup
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from lbms_app.models import Group as LbmsGroup, Category, Source, Expense

User = get_user_model()

SUPERUSER_USERNAME = 'hexwell'

USERS = (
    'meri',
    'enrico',
    'ettore'
)

ETTORE_LBMS_GROUP_NAME = 'Ettore'
FAMILY_LBMS_GROUP_NAME = 'Famiglia'

PERMISSION_GROUP_NAME = 'Users'


def _init_lbms_groups():
    ettore_group = LbmsGroup.objects.filter(name=ETTORE_LBMS_GROUP_NAME)

    if not ettore_group:
        LbmsGroup(name=ETTORE_LBMS_GROUP_NAME).save()

    family_group = LbmsGroup.objects.filter(name=FAMILY_LBMS_GROUP_NAME)

    if not (ettore_group and family_group):
        LbmsGroup(name=FAMILY_LBMS_GROUP_NAME).save()


def _init_superuser():
    user = User.objects.filter(is_superuser=True)

    if user:
        user = user.first()

    else:
        user = User.objects.create_superuser(
            SUPERUSER_USERNAME,
            password=getpass(f'Password for {SUPERUSER_USERNAME}: '),
            lbms_group=LbmsGroup.objects.get(name=ETTORE_LBMS_GROUP_NAME)
        )

    user.user_permissions.set(Permission.objects.all())

    user.save()


def _init_users():
    for u in USERS:
        user = User.objects.filter(username=u)

        if not user:
            User.objects.create_user(
                username=u,
                password=getpass(f'Password for {u}: '),
                lbms_group=LbmsGroup.objects.get(name=FAMILY_LBMS_GROUP_NAME),
                is_staff=True
            ).save()


def _init_permission_group():
    group = PermissionsGroup.objects.filter(name=PERMISSION_GROUP_NAME)

    if group:
        group = group.first()

    else:
        group = PermissionsGroup(name=PERMISSION_GROUP_NAME)
        group.save()

        for m in (Category, Source, Expense):
            ct = ContentType.objects.get_for_model(m)
            ps = Permission.objects.filter(content_type=ct)
            group.permissions.add(*ps)

        group.save()

    for user in User.objects.all():
        user.groups.add(group)


class Command(BaseCommand):
    help = f'Initialize LBMS'

    def handle(self, *args, **options):
        _init_lbms_groups()
        _init_superuser()
        _init_users()
        _init_permission_group()
