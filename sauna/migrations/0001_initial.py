# Generated by Django 3.2.5 on 2021-08-13 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50)),
                ('privilege', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('fill', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=5)),
                ('rest', models.DecimalField(decimal_places=2, max_digits=5)),
                ('person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sauna.person')),
            ],
        ),
    ]