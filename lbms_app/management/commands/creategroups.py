from django.core.management import BaseCommand

from lbms_app.models import Group

ETTORE_GROUP_NAME = 'Ettore'
FAMILY_GROUP_NAME = 'Famiglia'


class Command(BaseCommand):
    help = f'Create {ETTORE_GROUP_NAME} and {FAMILY_GROUP_NAME} groups'

    def __apply_group(self):
        pass

    def handle(self, *args, **options):
        ettore_group = Group.objects.filter(name=ETTORE_GROUP_NAME)
        family_group = Group.objects.filter(name=FAMILY_GROUP_NAME)

        if not (ettore_group and family_group):
            Group(name=ETTORE_GROUP_NAME).save()
            Group(name=FAMILY_GROUP_NAME).save()
