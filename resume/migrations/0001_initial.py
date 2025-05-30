# Generated by Django 5.2 on 2025-04-11 07:37

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Resume",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="작성일자"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="작성일자"
                    ),
                ),
                (
                    "resume_id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="id",
                    ),
                ),
                (
                    "education",
                    models.CharField(max_length=20, verbose_name="학력 사항"),
                ),
                ("introduce", models.TextField(verbose_name="자기소개서")),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resumes",
                        to="user.userinfo",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
