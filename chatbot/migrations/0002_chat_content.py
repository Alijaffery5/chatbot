# Generated by Django 5.1.2 on 2024-10-24 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='content',
            field=models.TextField(default='No content'),
        ),
    ]
