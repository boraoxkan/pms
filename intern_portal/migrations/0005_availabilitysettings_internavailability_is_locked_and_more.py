# Generated by Django 5.2.3 on 2025-07-18 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "intern_portal",
            "0004_alter_intern_options_intern_assigned_projects_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="AvailabilitySettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "minimum_hours_required",
                    models.PositiveIntegerField(
                        default=30,
                        help_text="Minimum total hours an intern must select per week",
                        verbose_name="Minimum Required Hours",
                    ),
                ),
                (
                    "weekly_submission_enabled",
                    models.BooleanField(
                        default=True,
                        help_text="If enabled, interns can only submit once per week",
                        verbose_name="Enable Weekly Submission Limit",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Availability System Settings",
                "verbose_name_plural": "Availability System Settings",
            },
        ),
        migrations.AddField(
            model_name="internavailability",
            name="is_locked",
            field=models.BooleanField(
                default=False,
                help_text="If true, intern cannot modify until admin unlocks",
            ),
        ),
        migrations.AddField(
            model_name="internavailability",
            name="submission_date",
            field=models.DateTimeField(
                blank=True,
                help_text="When this availability was last submitted",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="internavailability",
            name="week_year",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Week number and year (YYYYWW format) when this was submitted",
                null=True,
            ),
        ),
    ]
