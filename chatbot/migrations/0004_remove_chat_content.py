# Generated by Django 5.1.2 on 2024-10-24 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_chat_session_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='content',
        ),
    ]
