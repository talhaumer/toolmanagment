from django.db import transaction
from rest_framework import serializers

from tools.models import Tools, UserTools, GetBackSignature


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tools
        fields = ['id', 'name', 'model', 'manufacturer', 'date_of_purchase',
                  'cost', 'cost_depreciation_percentage_per_year', 'initial_location',
                  'calibrated_date', 'next_calibration_due_date', 'serial_number', 'created_on'
                  ]

    id = serializers.IntegerField(read_only=True)
    serial_number = serializers.CharField(required=True, max_length=50)
    name = serializers.CharField(required=True, max_length=50)
    model = serializers.CharField(required=True, max_length=50)
    manufacturer = serializers.CharField(required=True, max_length=50)
    date_of_purchase = serializers.DateField(required=True)
    cost = serializers.IntegerField(required=True)
    cost_depreciation_percentage_per_year = serializers.IntegerField(required=True)
    initial_location = serializers.CharField(required=True, max_length=50)
    calibrated_date = serializers.DateField(required=True)
    next_calibration_due_date = serializers.DateField(required=True)

    def create(self, validated_data):
        try:
            with transaction.atomic():
                tools = Tools.objects.create(**validated_data)
                return tools
        except:
            raise serializers.ValidationError("Product Didn't add to system")


class ToolAllocation(serializers.ModelSerializer):
    class Meta:
        model = UserTools
        fields = ['tool_id', 'return_date', 'location_of_work',
                  'tool_name', 'created_on']

    tool_name = serializers.CharField(read_only=True)
    tool_id = serializers.IntegerField(required=True, write_only=True)
    return_date = serializers.DateField(required=True)
    signature = serializers.ImageField(required=False)

    def create(self, validated_data):
        try:
            with transaction.atomic():
                tools = UserTools.objects.create(**validated_data)
                return tools
        except Exception as e:
            raise serializers.ValidationError("Tool didn't allocate")


class GetBackSerializers(serializers.ModelSerializer):
    class Meta:
        model = GetBackSignature
        fields = ['tool_id', 'back_signature', 'created_on']

    tool_id = serializers.IntegerField(required=True, write_only=True)
    back_signature = serializers.ImageField(required=False)
    created_on = serializers.DateField(read_only=True)

    def create(self, validated_data):
        try:
            with transaction.atomic():
                tools = GetBackSignature.objects.create(**validated_data)
                return tools
        except Exception as e:
            raise serializers.ValidationError("Tool operation not performed")


class UserAllocationHistory(serializers.ModelSerializer):
    class Meta:
        model = GetBackSignature
        fields = ['back_signature', 'tool', 'user', 'return_date', 'location_of_work', 'signature']

    tool = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    back_signature = serializers.SerializerMethodField(read_only=True)
    return_date = serializers.DateField(read_only=True)
    location_of_work = serializers.CharField(read_only=True)
    signature = serializers.CharField(read_only=True)

    def get_tool(self, obj):
        try:
            return obj.tool.name
        except:
            return None

    def get_user(self, obj):
        try:
            return f'{obj.user.first_name} {obj.user.last_name}'
        except:
            return None

    def get_back_signature(self, obj):
        try:
            back = GetBackSignature.objects.get(user_signature_back__tool_id=obj.id)
            return GetBackSerializers(back, many=True).data
        except:
            return None

