# Generated by Django 4.1.7 on 2023-05-09 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pbl5app', '0007_listencode_deleted_alter_listencode_encode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_user', models.IntegerField(blank=True, null=True)),
                ('encode_user', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='ListEncode',
        ),
    ]
