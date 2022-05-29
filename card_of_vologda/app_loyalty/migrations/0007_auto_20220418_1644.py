# Generated by Django 3.2.13 on 2022-04-18 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_loyalty', '0006_auto_20220418_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='категория')),
            ],
        ),
        migrations.AlterField(
            model_name='discount',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discount', to='app_loyalty.organization', verbose_name='организация'),
        ),
        migrations.AddField(
            model_name='organization',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='organization', to='app_loyalty.category', verbose_name='категория'),
            preserve_default=False,
        ),
    ]
