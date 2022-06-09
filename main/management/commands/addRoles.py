from user.models import AccessLevel, Role
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """command for creating roles"""
    roles = AccessLevel.DICT

    def handle(self, *args, **kwargs):
        for acl, role in self.roles.items():
            print(acl, role)
            role_object = Role.objects.filter(name=role, access_level=acl)
            if role_object.exists():
                print(f'{role} exists')
                continue
            else:
                r = Role(name=role, access_level=acl)
                r.save()
                print(f'{role} newly added.')
        print('All above roles have been added/updated successfully.')
