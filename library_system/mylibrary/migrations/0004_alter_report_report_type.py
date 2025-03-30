# Generated by Django 5.1.7 on 2025-03-30 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylibrary', '0003_librarian_member_report_transaction_penalty_manages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report_type',
            field=models.CharField(choices=[('borrowed', 'Borrowed Books'), ('overdue', 'Overdue Books'), ('returned', 'Returned Books')], max_length=20),
        ),
    ]
