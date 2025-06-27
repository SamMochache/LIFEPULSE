from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import (
    HeartRateRecord,
    BloodPressureRecord,
    BloodSugarRecord,
    BodyTemperatureRecord,
    Reminder,
    SpO2Record,
    
)

@shared_task
def send_html_email_task(to_email, subject, message, vital_type, value_display, username):
    html_content = render_to_string("emails/health_alert.html", {
        "user_name": username,
        "vital_type": vital_type,
        "value": value_display,
        "year": datetime.now().year,
    })

    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)

@shared_task
def send_daily_summary_emails():
    User = get_user_model()
    for user in User.objects.all():
        if not user.email:
            continue

        today = datetime.today().date()
        # You can expand this to include other vitals
        summary = {
            "heart_rate": HeartRateRecord.objects.filter(user=user, date=today).last(),
            "blood_pressure": BloodPressureRecord.objects.filter(user=user, date=today).last(),
            "blood_sugar": BloodSugarRecord.objects.filter(user=user, date=today).last(),
            "temperature": BodyTemperatureRecord.objects.filter(user=user, date=today).last(),
            "spo2": SpO2Record.objects.filter(user=user, date=today).last(),
        }

        html_content = render_to_string("emails/daily_summary.html", {
            "user": user,
            "summary": summary,
            "date": today,
            "year": today.year,
        })

        email = EmailMultiAlternatives(
            subject="📊 Daily Health Summary",
            body="Your daily health summary is available.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=True)

@shared_task
def send_due_reminders():
    now = timezone.now()
    window_start = now - timedelta(minutes=5)

    due_reminders = Reminder.objects.filter(
        remind_at__gte=window_start,
        remind_at__lte=now,
        notified=False
    )

    for reminder in due_reminders:
        subject = "⏰ Health Reminder"
        message = reminder.message
        html_content = render_to_string("emails/reminder.html", {
            "user_name": reminder.user.first_name or reminder.user.username,
            "message": reminder.message,
            "reminder_type": reminder.get_reminder_type_display(),
            "year": now.year,
        })

        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[reminder.user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=True)

        reminder.notified = True
        reminder.save()

@shared_task
def send_verification_email_task(email, subject, verification_link):
    text_content = f"Hi there,\nPlease click the link below to verify your email:\n{verification_link}"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
      <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h2 style="color: #2c3e50;">Welcome to LifePulse!</h2>
        <p style="font-size: 16px; color: #333;">
          Thank you for registering. Please verify your email address by clicking the button below:
        </p>
        <div style="text-align: center; margin: 30px 0;">
          <a href="{verification_link}" style="background-color: #27ae60; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">
            Verify My Email
          </a>
        </div>
        <p style="font-size: 14px; color: #777;">
          If you didn’t request this, you can safely ignore this email.
        </p>
        <hr style="margin-top: 30px;">
        <p style="font-size: 12px; color: #999;">&copy; 2025 LifePulse. All rights reserved.</p>
      </div>
    </body>
    </html>
    """

    email_msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()