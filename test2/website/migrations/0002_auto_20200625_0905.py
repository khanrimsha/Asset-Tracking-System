# Generated by Django 3.0.7 on 2020-06-25 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('lat', models.IntegerField(max_length=20)),
                ('long', models.IntegerField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='Incidences',
        ),
    ]
