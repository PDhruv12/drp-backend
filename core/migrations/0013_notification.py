# Generated by Django 5.2.1 on 2025-06-15 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_usersmessage_usersmessageimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notification_id', models.AutoField(primary_key=True, serialize=False)),
                ('notification_type', models.CharField(choices=[('say_hi', 'Say Hi'), ('joined_community', 'Joined Community'), ('dm_message', 'Direct Message'), ('community_message', 'Community Message')], max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('community', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.community')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='core.usertable')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_notifications', to='core.usertable')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
