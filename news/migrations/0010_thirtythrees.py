# Generated by Django 3.2 on 2022-05-25 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_topwordsbyorg'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThirtyThrees',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('headline', models.CharField(max_length=200)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
