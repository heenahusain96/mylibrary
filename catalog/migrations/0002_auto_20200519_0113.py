# Generated by Django 3.0.5 on 2020-05-18 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='summary',
            field=models.TextField(blank=True, help_text='Enter a brief description of the book', max_length=1000, null=True),
        ),
    ]
