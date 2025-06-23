from django.db import models
from django.conf import settings
from users.models import User

class Vitals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    heart_rate = models.IntegerField()
    systolic_bp = models.IntegerField()
    diastolic_bp = models.IntegerField()
    blood_sugar = models.FloatField(null=True, blank=True)
    oxygen_saturation = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vitals for {self.user.username} at {self.date_recorded}"


class SleepRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    hours_slept = models.FloatField()
    sleep_quality = models.CharField(max_length=20, choices=[('poor', 'Poor'), ('average', 'Average'), ('good', 'Good')])

    def __str__(self):
        return f"{self.user.username} - {self.date} Sleep"


class WeightRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight_kg = models.FloatField()

    @property
    def bmi(self):
        return round(self.weight_kg / (1.75 ** 2), 2)  # Example: replace with real height logic

    def __str__(self):
        return f"{self.user.username} - {self.date} Weight"


class BloodSugarRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    fasting = models.FloatField()
    post_meal = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.date} Sugar"

class BloodPressureRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    systolic = models.IntegerField()
    diastolic = models.IntegerField()
    pulse = models.IntegerField()
    
    def __str__(self):
        return f"{self.user.username} - {self.date} BP"

class HeartRateRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    resting_hr = models.IntegerField()
    high_hr = models.IntegerField()
    low_hr = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.date} HR"

class StepCountRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    steps = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user} - {self.steps} steps on {self.date}"

class SpO2Record(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    spo2 = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 98.75%

    def __str__(self):
        return f"{self.user} - SpO2 {self.spo2}% on {self.date}"

class BodyTemperatureRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1)  # e.g., 37.2°C

    def __str__(self):
        return f"{self.user} - Temp {self.temperature}°C on {self.date}"