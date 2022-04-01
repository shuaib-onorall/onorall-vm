# Generated by Django 3.2.12 on 2022-04-01 11:50

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_auto_20220401_0447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresources',
            name='resourcesid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='basic_branding',
            name='brandingid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='basic_display',
            name='highlightid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='connect',
            name='connectid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='connect_comment',
            name='commentid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='detail',
            name='videoid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='doc_verification',
            name='docid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='groupskillid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='grouplistid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='textid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='question2',
            name='qnaid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='question3',
            name='mcqid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='questionnaires',
            name='questionnaireid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='report4',
            name='reportid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='sectionid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='sign',
            name='id',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='social_handling',
            name='socialid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='timelinemodel',
            name='resourcesid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='workbaseinfo',
            name='wbid',
            field=models.CharField(default=myapp.models.random_id_field, max_length=12, unique=True),
        ),
    ]
