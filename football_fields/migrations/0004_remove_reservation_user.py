# Generated by Django 5.0.7 on 2024-08-02 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football_fields', '0003_alter_footballfield_latitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='user',
        ),
    ]