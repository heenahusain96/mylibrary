# Generated by Django 3.0.5 on 2020-07-28 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20200728_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinstance',
            name='user_book_review',
            field=models.TextField(blank=True, help_text='Enter a review of the book', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='summary',
            field=models.TextField(blank=True, help_text='Enter a brief description of the book', max_length=300, null=True),
        ),
    ]