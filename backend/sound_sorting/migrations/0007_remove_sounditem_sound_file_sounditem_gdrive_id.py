# Generated by Django 4.0.4 on 2023-03-21 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sound_sorting', '0006_alter_sounditemreview_categories_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sounditem',
            name='sound_file',
        ),
        migrations.AddField(
            model_name='sounditem',
            name='gdrive_id',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
