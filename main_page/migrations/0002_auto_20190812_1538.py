# Generated by Django 2.2.4 on 2019-08-12 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='corso',
            old_name='op_id',
            new_name='operatore',
        ),
        migrations.RenameField(
            model_name='prenota',
            old_name='user_id',
            new_name='user',
        ),
    ]