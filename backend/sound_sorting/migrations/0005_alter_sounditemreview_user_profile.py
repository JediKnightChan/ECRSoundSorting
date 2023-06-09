# Generated by Django 4.0.4 on 2023-03-19 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0001_initial'),
        ('sound_sorting', '0004_alter_soundcategory_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sounditemreview',
            name='user_profile',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='sound_reviews', to='myauth.userprofile'),
            preserve_default=False,
        ),
    ]
