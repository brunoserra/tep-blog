# Generated by Django 2.0.7 on 2018-08-01 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.CharField(max_length=255),
        ),
    ]
