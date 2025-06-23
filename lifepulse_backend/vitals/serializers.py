from rest_framework import serializers
from .models import Vitals, SleepRecord, WeightRecord, HeartRateRecord, BloodPressureRecord, BloodSugarRecord, StepCountRecord, SpO2Record, BodyTemperatureRecord

class VitalsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Vitals
        fields = '__all__'
        read_only_fields = ['user']

class SleepRecordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = SleepRecord
        fields = '__all__'

class WeightRecordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    bmi = serializers.ReadOnlyField()
    class Meta:
        model = WeightRecord
        fields = '__all__'

class HeartRateRecordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = HeartRateRecord
        fields = '__all__'

class BloodPressureRecordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = BloodPressureRecord
        fields = '__all__'

class BloodSugarRecordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = BloodSugarRecord
        fields = '__all__'


class StepCountRecordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = StepCountRecord
        fields = '__all__'
        read_only_fields = ['user']

class SpO2RecordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SpO2Record
        fields = '__all__'
        read_only_fields = ['user']

class BodyTemperatureRecordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = BodyTemperatureRecord
        fields = '__all__'
        read_only_fields = ['user']