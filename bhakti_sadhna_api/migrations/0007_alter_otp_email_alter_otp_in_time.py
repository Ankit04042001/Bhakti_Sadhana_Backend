# Generated by Django 4.1.3 on 2023-02-07 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bhakti_sadhna_api', '0006_remove_otp_punch_in_remove_otp_user_otp_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='email',
            field=models.EmailField(editable=False, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='otp',
            name='in_time',
            field=models.TimeField(default='19:19:25', editable=False),
        ),
    ]
