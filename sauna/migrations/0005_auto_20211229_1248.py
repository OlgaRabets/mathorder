# Generated by Django 3.2.5 on 2021-12-29 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sauna', '0004_rename_person_id_visit_person'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['name'], 'verbose_name': 'Посетителя', 'verbose_name_plural': 'Посетители'},
        ),
        migrations.AlterModelOptions(
            name='price',
            options={'ordering': ['privilege', 'number'], 'verbose_name': 'Тариф', 'verbose_name_plural': 'Тарифы'},
        ),
        migrations.AlterModelOptions(
            name='visit',
            options={'ordering': ['-date', 'person'], 'verbose_name': 'Посещение', 'verbose_name_plural': 'Посещения'},
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(db_index=True, max_length=50, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='person',
            name='privilege',
            field=models.BooleanField(verbose_name='Льготный тариф'),
        ),
        migrations.AlterField(
            model_name='price',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Стоимость'),
        ),
        migrations.AlterField(
            model_name='price',
            name='number',
            field=models.IntegerField(verbose_name='Номер посещения в месяце'),
        ),
        migrations.AlterField(
            model_name='price',
            name='privilege',
            field=models.BooleanField(verbose_name='Льготный тариф'),
        ),
        migrations.AlterField(
            model_name='visit',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Стоимость'),
        ),
        migrations.AlterField(
            model_name='visit',
            name='date',
            field=models.DateField(verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='visit',
            name='fill',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Пополнение'),
        ),
        migrations.AlterField(
            model_name='visit',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sauna.person', verbose_name='Посетитель'),
        ),
        migrations.AlterField(
            model_name='visit',
            name='rest',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Остаток'),
        ),
    ]