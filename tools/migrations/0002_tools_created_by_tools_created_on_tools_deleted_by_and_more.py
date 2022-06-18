# Generated by Django 4.0.5 on 2022-06-18 06:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tools',
            name='created_by',
            field=models.BigIntegerField(blank=True, db_column='CreatedBy', default=0, null=True),
        ),
        migrations.AddField(
            model_name='tools',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, db_column='CreatedOn', default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tools',
            name='deleted_by',
            field=models.BigIntegerField(blank=True, db_column='DeletedBy', default=0, null=True),
        ),
        migrations.AddField(
            model_name='tools',
            name='deleted_on',
            field=models.DateTimeField(auto_now=True, db_column='DeletedOn'),
        ),
        migrations.AddField(
            model_name='tools',
            name='modified_by',
            field=models.BigIntegerField(blank=True, db_column='ModifiedBy', default=0, null=True),
        ),
        migrations.AddField(
            model_name='tools',
            name='modified_on',
            field=models.DateTimeField(auto_now=True, db_column='ModifiedOn'),
        ),
        migrations.AddField(
            model_name='tools',
            name='status',
            field=models.BigIntegerField(db_column='Status', default=0, help_text='Be default 0 which has no meaning this field is used for making the status like pending approved and for some other purpose'),
        ),
        migrations.AddField(
            model_name='usersignature',
            name='created_by',
            field=models.BigIntegerField(blank=True, db_column='CreatedBy', default=0, null=True),
        ),
        migrations.AddField(
            model_name='usersignature',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, db_column='CreatedOn', default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usersignature',
            name='deleted_by',
            field=models.BigIntegerField(blank=True, db_column='DeletedBy', default=0, null=True),
        ),
        migrations.AddField(
            model_name='usersignature',
            name='deleted_on',
            field=models.DateTimeField(auto_now=True, db_column='DeletedOn'),
        ),
        migrations.AddField(
            model_name='usersignature',
            name='modified_by',
            field=models.BigIntegerField(blank=True, db_column='ModifiedBy', default=0, null=True),
        ),
        migrations.AddField(
            model_name='usersignature',
            name='modified_on',
            field=models.DateTimeField(auto_now=True, db_column='ModifiedOn'),
        ),
        migrations.AddField(
            model_name='usersignature',
            name='status',
            field=models.BigIntegerField(db_column='Status', default=0, help_text='Be default 0 which has no meaning this field is used for making the status like pending approved and for some other purpose'),
        ),
        migrations.AddField(
            model_name='usertools',
            name='created_by',
            field=models.BigIntegerField(blank=True, db_column='CreatedBy', default=0, null=True),
        ),
        migrations.AddField(
            model_name='usertools',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, db_column='CreatedOn', default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usertools',
            name='deleted_by',
            field=models.BigIntegerField(blank=True, db_column='DeletedBy', default=0, null=True),
        ),
        migrations.AddField(
            model_name='usertools',
            name='deleted_on',
            field=models.DateTimeField(auto_now=True, db_column='DeletedOn'),
        ),
        migrations.AddField(
            model_name='usertools',
            name='modified_by',
            field=models.BigIntegerField(blank=True, db_column='ModifiedBy', default=0, null=True),
        ),
        migrations.AddField(
            model_name='usertools',
            name='modified_on',
            field=models.DateTimeField(auto_now=True, db_column='ModifiedOn'),
        ),
        migrations.AddField(
            model_name='usertools',
            name='status',
            field=models.BigIntegerField(db_column='Status', default=0, help_text='Be default 0 which has no meaning this field is used for making the status like pending approved and for some other purpose'),
        ),
        migrations.CreateModel(
            name='GetBackSignature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.BigIntegerField(blank=True, db_column='CreatedBy', default=0, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='CreatedOn')),
                ('modified_by', models.BigIntegerField(blank=True, db_column='ModifiedBy', default=0, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, db_column='ModifiedOn')),
                ('deleted_by', models.BigIntegerField(blank=True, db_column='DeletedBy', default=0, null=True)),
                ('deleted_on', models.DateTimeField(auto_now=True, db_column='DeletedOn')),
                ('status', models.BigIntegerField(db_column='Status', default=0, help_text='Be default 0 which has no meaning this field is used for making the status like pending approved and for some other purpose')),
                ('signature', models.ImageField(upload_to='')),
                ('user_signature_back', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_signature_back', to='tools.usersignature')),
            ],
            options={
                'db_table': 'GetBackSignature',
            },
        ),
    ]
