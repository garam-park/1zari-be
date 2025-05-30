# Generated by Django 5.2 on 2025-04-14 08:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resume", "0005_alter_careerinfo_employment_period_end"),
    ]

    operations = [
        migrations.AlterField(
            model_name="careerinfo",
            name="resume",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="careers",
                to="resume.resume",
            ),
        ),
    ]
