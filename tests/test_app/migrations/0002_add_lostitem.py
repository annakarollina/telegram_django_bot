# Migration para o modelo LostItem (achados e perdidos)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LostItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='lost_items/')),
                ('description', models.TextField(blank=True)),
                ('telegram_user_id', models.BigIntegerField()),
                ('is_complete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'LostItem',
                'verbose_name_plural': 'LostItems',
            },
        ),
    ]
