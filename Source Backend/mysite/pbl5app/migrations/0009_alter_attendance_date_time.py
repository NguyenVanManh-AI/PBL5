# Generated by Django 4.1.7 on 2023-05-13 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pbl5app', '0008_encode_delete_listencode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date_time',
            field=models.DateTimeField(),
        ),
    ]