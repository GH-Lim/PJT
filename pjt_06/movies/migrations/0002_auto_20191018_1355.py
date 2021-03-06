# Generated by Django 2.2.6 on 2019-10-18 04:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='score',
            field=models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MaxValueValidator(limit_value=10, message='10 이하의 수를 입력해주세요')]),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('score', models.IntegerField(validators=[django.core.validators.MaxValueValidator(limit_value=10, message='10 이하의 수를 입력해주세요')])),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='movies.Movie')),
            ],
            options={
                'ordering': ('-pk',),
            },
        ),
    ]
