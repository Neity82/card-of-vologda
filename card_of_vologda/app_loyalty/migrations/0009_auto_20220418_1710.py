# Generated by Django 3.2.13 on 2022-04-18 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_loyalty', '0008_discount_created_up'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='discount',
            options={'ordering': ['-created_up'], 'verbose_name': 'скидка', 'verbose_name_plural': 'скидки'},
        ),
        migrations.AlterModelTable(
            name='category',
            table='categories',
        ),
    ]
