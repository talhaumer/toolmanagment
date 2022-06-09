# Generated by Django 4.0.5 on 2022-06-09 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.BigIntegerField(blank=True, db_column='CreatedBy', default=0, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='CreatedOn')),
                ('modified_by', models.BigIntegerField(blank=True, db_column='ModifiedBy', default=0, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, db_column='ModifiedOn')),
                ('deleted_by', models.BigIntegerField(blank=True, db_column='DeletedBy', default=0, null=True)),
                ('deleted_on', models.DateTimeField(auto_now=True, db_column='DeletedOn')),
                ('status', models.BigIntegerField(db_column='Status', default=0, help_text='Be default 0 which has no meaning this field is used for making the status like pending approved and for some other purpose')),
                ('name', models.CharField(db_column='Name', max_length=255, unique=True)),
                ('code', models.SlugField(db_column='Code', default='')),
                ('description', models.TextField(blank=True, db_column='Description', null=True)),
                ('access_level', models.IntegerField(choices=[(800, 'Admin'), (900, 'Super_Admin')], db_column='AccessLevel', default=800)),
            ],
            options={
                'db_table': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_by', models.BigIntegerField(blank=True, db_column='CreatedBy', default=0, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='CreatedOn')),
                ('modified_by', models.BigIntegerField(blank=True, db_column='ModifiedBy', default=0, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, db_column='ModifiedOn')),
                ('deleted_by', models.BigIntegerField(blank=True, db_column='DeletedBy', default=0, null=True)),
                ('deleted_on', models.DateTimeField(auto_now=True, db_column='DeletedOn')),
                ('status', models.BigIntegerField(db_column='Status', default=0, help_text='Be default 0 which has no meaning this field is used for making the status like pending approved and for some other purpose')),
                ('name', models.CharField(db_column='Name', default='', max_length=255)),
                ('is_active', models.BooleanField(db_column='IsActive', default=True, help_text='Designates whether this user should be treated as active.')),
                ('email', models.EmailField(db_column='Email', help_text='Email Field', max_length=254, unique=True)),
                ('is_approved', models.BooleanField(db_column='IsApproved', default=False, help_text='Designates whether this user is approved or not.')),
                ('is_staff', models.BooleanField(default=True, help_text='Designates whether the user can log into this admin site.')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('role', models.ForeignKey(db_column='RoleId', default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_role', to='user.role')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
