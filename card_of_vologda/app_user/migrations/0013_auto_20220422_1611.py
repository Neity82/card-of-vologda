# Generated by Django 3.2.13 on 2022-04-22 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0012_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True),
        ),
    ]