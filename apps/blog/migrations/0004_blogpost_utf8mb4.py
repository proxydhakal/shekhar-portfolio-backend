# Migration to fix MySQL OperationalError 1366: allow full UTF-8 (e.g. box-drawing │) in content

from django.db import migrations


def convert_to_utf8mb4(apps, schema_editor):
    """Convert blog_blogpost table to utf8mb4 so content accepts all UTF-8 (e.g. │ in code blocks)."""
    if schema_editor.connection.vendor != "mysql":
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            "ALTER TABLE blog_blogpost CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_add_blog_seo_meta"),
    ]

    operations = [
        migrations.RunPython(convert_to_utf8mb4, noop),
    ]
