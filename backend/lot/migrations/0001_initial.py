# Generated by Django 3.1 on 2021-10-15 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auction', '0001_initial'),
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auction.auction')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.item')),
            ],
        ),
    ]
