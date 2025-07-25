# Generated by Django 5.2.3 on 2025-07-19 08:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('current_weight', models.FloatField(blank=True, null=True)),
                ('goal', models.CharField(blank=True, choices=[('lose_weight', 'Lose Weight'), ('gain_muscle', 'Gain Muscle'), ('improve_health', 'Imporve Health'), ('maintain', 'Maintain Weight')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
