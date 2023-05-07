# Generated by Django 4.2.1 on 2023-05-07 12:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_alter_friendshiprequests_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friends',
            name='first_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendshiprequests',
            name='status',
            field=models.CharField(default='has been sent', max_length=15),
        ),
    ]
