from django import forms
from .models import Article, Commentaire, Reponse


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'image', 'video']

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')

        if image and video:
            raise forms.ValidationError('Un article ne peut pas contenir à la fois une image et une vidéo')

        return cleaned_data


class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['contenu']


class ReponseForm(forms.ModelForm):
    class Meta:
        model = Reponse
        fields = ['contenu']
