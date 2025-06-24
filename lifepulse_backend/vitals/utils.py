from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from .models import Alert
from .tasks import send_html_email_task  # Celery task

def trigger_alert(user, vital_type, value, thresholds, message_template):
    def send_html_email(subject, message, value_display):
        if not user.email:
            return

        # Use Celery task instead of direct sending
        send_html_email_task.delay(
            user.email,
            subject,
            message,
            vital_type,
            value_display,
            user.first_name or user.username,
        )

    if isinstance(value, tuple):  # For BP
        systolic, diastolic = value
        systolic_max = thresholds.get("systolic_max", 180)
        diastolic_max = thresholds.get("diastolic_max", 120)
        if systolic > systolic_max or diastolic > diastolic_max:
            message = message_template.format(systolic, diastolic)
            display = f"{systolic}/{diastolic} mmHg"
            Alert.objects.create(user=user, vital_type=vital_type, message=message)
            send_html_email("🩺 Health Alert: Blood Pressure", message, display)
    else:
        min_val = thresholds.get("min", float("-inf"))
        max_val = thresholds.get("max", float("inf"))
        if value < min_val or value > max_val:
            message = message_template.format(value)
            display = f"{value}"
            Alert.objects.create(user=user, vital_type=vital_type, message=message)
            send_html_email(f"🩺 Health Alert: {vital_type.title()}", message, display)
