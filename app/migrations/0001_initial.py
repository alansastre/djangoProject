# Generated by Django 3.2.3 on 2021-05-19 11:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(default='support@library.com', max_length=254)),
                ('num_books', models.IntegerField(default=1)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('married', models.BooleanField(default=False)),
                ('salary', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'authors',
            },
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=100)),
                ('province', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'directions',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=150)),
                ('year', models.IntegerField(default=0)),
                ('published', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.author')),
            ],
            options={
                'db_table': 'books',
            },
        ),
        migrations.AddField(
            model_name='author',
            name='direction',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.direction'),
        ),
    ]