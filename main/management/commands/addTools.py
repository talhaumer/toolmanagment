import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction

from tools.models import Tools


class Command(BaseCommand):
    """command for creating roles"""
    data = pd.read_excel('/home/talha-umer/backend/products/managment/commands/Tools List for Talha.xlsx')
    data = data.to_dict('records')

    def handle(self, *args, **kwargs):
        for each in self.data:
            del each["#"]
            with transaction.atomic():
                x = Tools.objects.get_or_create(**each)
                if x[1] == False:
                    print("Tool Already Exsist")
                else:
                    print("Tool added successfully")
        print('All above roles have been added/updated successfully.')
