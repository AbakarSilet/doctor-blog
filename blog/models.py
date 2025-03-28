from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import os


def validate_image_size(value):
    if value.size > 10 * 1024 * 1024:  # 10MB
        raise ValidationError('La taille de l\'image ne doit pas dépasser 10MB')


def validate_video_size(value):
    if value.size > 20 * 1024 * 1024:  # 20MB
        raise ValidationError('La taille de la vidéo ne doit pas dépasser 20MB')


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    valid_video_extensions = ['.mp4', '.mov', '.avi']
    if ext.lower() not in valid_image_extensions + valid_video_extensions:
        raise ValidationError('Format de fichier non supporté')


class Article(models.Model):
    titre = models.CharField(max_length=500)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, max_length=500)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='articles_likes', blank=True)
    image = models.ImageField(
        upload_to='articles/images/',
        null=True,
        blank=True,
        validators=[validate_image_size, validate_file_extension]
    )
    video = models.FileField(
        upload_to='articles/videos/',
        null=True,
        blank=True,
        validators=[validate_video_size, validate_file_extension]
    )

    def clean(self):
        if self.image and self.video:
            raise ValidationError('Un article ne peut pas contenir à la fois une image et une vidéo')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        self.clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre


class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_commentaires', blank=True)

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-date_creation']

    def __str__(self):
        return self.contenu

    def total_likes(self):
        return self.likes.count()


class Reponse(models.Model):
    commentaire = models.ForeignKey(Commentaire, on_delete=models.CASCADE, related_name='reponses')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_creation']
