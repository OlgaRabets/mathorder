# Generated by Django 3.2.5 on 2021-09-30 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sauna', '0003_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visit',
            old_name='person_id',
            new_name='person',
        ),
    ]
