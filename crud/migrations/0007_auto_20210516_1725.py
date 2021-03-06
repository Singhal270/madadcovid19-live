# Generated by Django 3.1.4 on 2021-05-16 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0006_auto_20210516_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='Number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='description',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
