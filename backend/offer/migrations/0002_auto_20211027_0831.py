# Generated by Django 3.1 on 2021-10-27 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
