# Generated by Django 3.0.5 on 2020-05-20 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20200519_0116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='author',
            name='date_of_death',
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(default='default value', max_length=200),
            preserve_default=False,
        ),
    ]
