# Generated by Django 4.1.6 on 2023-02-13 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bhakti_sadhna_api', '0010_alter_attendence_date_alter_otp_in_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='in_time',
            field=models.TimeField(default='23:17:42', editable=False),
        ),
    ]
