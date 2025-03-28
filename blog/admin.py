from django.contrib import admin
from .models import Article, Commentaire, Reponse


class CommentaireInline(admin.TabularInline):
    model = Commentaire
    extra = 1  # Nombre de nouveaux commentaires à ajouter par défaut


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_creation', 'date_modification')
    prepopulated_fields = {'slug': ('titre',)}
    inlines = [CommentaireInline]


class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('contenu', 'auteur', 'article')


class ReponseAdmin(admin.ModelAdmin):
    list_display = ('contenu', 'auteur')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Reponse, ReponseAdmin)
admin.site.register(Commentaire, CommentaireAdmin)
