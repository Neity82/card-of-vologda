# Generated by Django 3.2.13 on 2022-04-15 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_loyalty', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-created_up'], 'verbose_name': 'новость', 'verbose_name_plural': 'новости'},
        ),
        migrations.AddField(
            model_name='news',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активна'),
        ),
        migrations.AddField(
            model_name='organization',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активна'),
        ),
    ]
