# Generated by Django 3.2.13 on 2022-04-18 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_loyalty', '0012_auto_20220418_1756'),
        ('app_user', '0006_alter_customuser_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='app_loyalty.organization', verbose_name='организация'),
        ),
    ]
