from django.db import models

# Create your models here.
from main.models import Base
from user.models import User


class Tools(Base):
    name = models.CharField(max_length=250, blank=True, null=True)
    manufacturer = models.CharField(max_length=250, blank=True, null=True)
    model = models.CharField(max_length=250, blank=True, null=True)
    serial_number = models.CharField(max_length=250, blank=True, null=True)
    date_of_purchase = models.DateField()
    calibrated_date = models.DateField()
    next_calibration_due_date = models.DateField()
    cost = models.IntegerField(blank=True, null=True)
    cost_depreciation_percentage_per_year = models.IntegerField(blank=True, null=True)
    initial_location = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        db_table = "Tools"


class UserTools(Base):
    tool = models.ForeignKey(Tools, related_name="allocated_tools", on_delete=models.CASCADE)
    user_account = models.ForeignKey(User, related_name="user_tool", on_delete=models.CASCADE)
    return_date = models.DateField()
    location_of_work = models.CharField(max_length=250, blank=True, null=True)
    allocated = models.BooleanField(default=False)
    signature = models.ImageField()

    class Meta:
        db_table = "UserTools"



class GetBackSignature(Base):
    user_signature_back = models.ForeignKey(UserTools, related_name="user_allocated_tool", on_delete=models.CASCADE)
    signature = models.ImageField()

    class Meta:
        db_table = "GetBackSignature"
