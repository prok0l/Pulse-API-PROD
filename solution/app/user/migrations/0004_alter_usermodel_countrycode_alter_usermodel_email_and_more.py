# Generated by Django 5.0.1 on 2024-02-29 14:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_usermodel_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='countryCode',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='email',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
