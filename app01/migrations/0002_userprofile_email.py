# Generated by Django 2.2.5 on 2020-02-07 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=25, null=True),
        ),
    ]
