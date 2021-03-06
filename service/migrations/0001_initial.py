# Generated by Django 4.0.4 on 2022-04-27 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription', models.CharField(choices=[('basic', 'basic'), ('business', 'business'), ('agency', 'agency')], max_length=20)),
                ('limit', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac', models.CharField(max_length=6)),
                ('vendor', models.CharField(max_length=255)),
            ],
        ),
    ]
