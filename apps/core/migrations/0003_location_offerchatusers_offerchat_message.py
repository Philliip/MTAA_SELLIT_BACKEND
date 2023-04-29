# Generated by Django 4.1.7 on 2023-03-24 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_psc_city_zip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('location_string', models.CharField(max_length=255, verbose_name='location_message')),
                ('location_coordinates', models.CharField(max_length=255, verbose_name='coordinates_message')),
            ],
            options={
                'db_table': 'locations',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='OfferChatUsers',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('owner', models.BooleanField(default=True)),
                ('offer_chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_chats', to='core.offer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'offers_chats_users',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='OfferChat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='core.offer')),
            ],
            options={
                'db_table': 'offers_chats',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('content', models.CharField(max_length=200, verbose_name='message_content')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='core.location')),
                ('offer_chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='core.offerchat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'messages',
                'default_permissions': (),
            },
        ),
    ]