# Generated by Django 5.1.3 on 2025-03-08 14:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='commentaire',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_commentaires', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Reponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('commentaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reponses', to='blog.commentaire')),
            ],
            options={
                'ordering': ['date_creation'],
            },
        ),
    ]
