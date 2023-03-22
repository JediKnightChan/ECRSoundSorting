# Generated by Django 4.0.4 on 2023-03-19 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0001_initial'),
        ('sound_sorting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoundItemReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_useful', models.BooleanField()),
                ('text_review', models.TextField(blank=True, max_length=50)),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('updated_ts', models.DateTimeField(auto_now=True)),
                ('categories', models.ManyToManyField(related_name='sound_reviews', to='sound_sorting.soundcategory')),
                ('user_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sound_reviews', to='myauth.userprofile')),
            ],
        ),
    ]