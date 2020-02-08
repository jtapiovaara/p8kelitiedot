# Generated by Django 3.0.3 on 2020-02-05 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32)),
            ],
            options={
                'verbose_name_plural': 'cities',
            },
        ),
    ]