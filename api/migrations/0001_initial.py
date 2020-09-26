# Generated by Django 3.0.8 on 2020-07-25 03:01

import api.models
import api.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SourceFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(blank=True, max_length=255, null=True, upload_to=api.models.source_file_path, validators=[api.validators.is_valid_size, api.validators.is_valid_audio_file])),
                ('is_youtube', models.BooleanField(default=False)),
                ('youtube_link', models.URLField(blank=True, null=True, unique=True, validators=[api.validators.is_valid_youtube])),
            ],
        ),
        migrations.CreateModel(
            name='SourceTrack',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('artist', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('source_file', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='api.SourceFile')),
            ],
        ),
        migrations.CreateModel(
            name='YTAudioDownloadTask',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.IntegerField(choices=[(0, 'Queued'), (1, 'In Progress'), (2, 'Done'), (-1, 'Error')], default=0)),
                ('error', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='sourcefile',
            name='youtube_fetch_task',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.YTAudioDownloadTask'),
        ),
        migrations.CreateModel(
            name='StaticMix',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('vocals', models.BooleanField()),
                ('drums', models.BooleanField()),
                ('bass', models.BooleanField()),
                ('other', models.BooleanField()),
                ('status', models.IntegerField(choices=[(0, 'Queued'), (1, 'In Progress'), (2, 'Done'), (-1, 'Error')], default=0)),
                ('file', models.FileField(blank=True, max_length=255, upload_to=api.models.mix_track_path)),
                ('error', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('source_track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='static', to='api.SourceTrack')),
            ],
            options={
                'unique_together': {('source_track', 'vocals', 'drums', 'bass', 'other')},
            },
        ),
        migrations.CreateModel(
            name='DynamicMix',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('vocals_file', models.FileField(blank=True, max_length=255, upload_to=api.models.mix_track_path)),
                ('other_file', models.FileField(blank=True, max_length=255, upload_to=api.models.mix_track_path)),
                ('bass_file', models.FileField(blank=True, max_length=255, upload_to=api.models.mix_track_path)),
                ('drums_file', models.FileField(blank=True, max_length=255, upload_to=api.models.mix_track_path)),
                ('status', models.IntegerField(choices=[(0, 'Queued'), (1, 'In Progress'), (2, 'Done'), (-1, 'Error')], default=0)),
                ('error', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('source_track', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dynamic', to='api.SourceTrack')),
            ],
            options={
                'unique_together': {('source_track',)},
            },
        ),
    ]