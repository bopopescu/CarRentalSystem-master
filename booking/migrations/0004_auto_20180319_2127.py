# Generated by Django 2.0.2 on 2018-03-19 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_car'),
    ]

    operations = [
        migrations.CreateModel(
            name='cars',
            fields=[
                ('company', models.CharField(max_length=15)),
                ('model_name', models.CharField(max_length=15)),
                ('car_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('seat', models.CharField(max_length=3)),
                ('hour_price', models.CharField(max_length=5)),
                ('type', models.CharField(max_length=15)),
                ('position', models.CharField(max_length=20)),
                ('images', models.CharField(max_length=15)),
            ],
        ),
        migrations.DeleteModel(
            name='car',
        ),
    ]
