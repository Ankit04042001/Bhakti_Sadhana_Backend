# Generated by Django 4.1.3 on 2023-02-07 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bhakti_sadhna_api', '0002_task_otp_attendence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='otp',
            field=models.IntegerField(max_length=6),
        ),
        migrations.AlterField(
            model_name='otp',
            name='punch_in',
            field=models.TimeField(default='14:12:11', editable=False),
        ),
    ]
