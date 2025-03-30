# Generated by Django 5.1.7 on 2025-03-30 06:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylibrary', '0002_rename_books_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='Librarian',
            fields=[
                ('librarian_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('membership_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('membership_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('membership_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False)),
                ('report_type', models.CharField(max_length=255)),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('details', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('borrow_date', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('return_date', models.DateField(blank=True, null=True)),
                ('overdue_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mylibrary.book')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mylibrary.member')),
            ],
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('penalty_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('paid_status', models.BooleanField(default=False)),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mylibrary.transaction')),
            ],
        ),
        migrations.CreateModel(
            name='Manages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mylibrary.book')),
                ('librarian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mylibrary.librarian')),
            ],
            options={
                'unique_together': {('librarian', 'book')},
            },
        ),
    ]
