# Generated by Django 4.2.1 on 2023-05-06 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friends',
            name='second_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accepted', to=settings.AUTH_USER_MODEL),
        ),
    ]
