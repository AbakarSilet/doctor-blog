from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from accounts.models import User
from .forms import ArticleForm, CommentaireForm
from .forms import ReponseForm
from .models import Article, Commentaire


# Fonction pour vérifier si l'utilisateur est admin
def is_admin(user):
    return user.groups.filter(name='Admin').exists()


# Décorateur pour vérifier si l'utilisateur est admin
def admin_required(view_func):
    decorated_view = user_passes_test(is_admin, login_url='403')(view_func)
    return decorated_view


def custom_404(request):
    return render(request, '404.html', status=404)


def custom_403(request):
    return render(request, '403.html', status=403)


@login_required
@admin_required
def transition_page(request):
    # Récupérer les statistiques
    nombre_articles = Article.objects.count()
    nombre_commentaires = Commentaire.objects.count()
    nombre_utilisateurs = User.objects.count()
    dernier_article = Article.objects.order_by('-date_creation').first()

    context = {
        'nombre_articles': nombre_articles,
        'nombre_commentaires': nombre_commentaires,
        'nombre_utilisateurs': nombre_utilisateurs,
        "dernier_article": dernier_article,
    }
    return render(request, 'transition.html', context)


def home(request):
    articles = Article.objects.all()[:3]
    return render(request, 'index.html',{'articles': articles})


def about(request):
    return render(request, 'about.html')


def portfolio(request):
    return render(request, 'work.html')


def contact(request):
    return render(request, 'contact.html')



def send_email(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        message = request.POST.get('user-message')

        formatted_message = message

        # print(f"""
        # ----- EMAIL SIMULÉ -----
        # De: {user_email}
        # Nom: {user_name}
        # À: lekamyangambibenido@gmail.com
        # Message: {formatted_message}
        # ----------------------
        # """)

        # Pour un vrai envoi d'email 
        send_mail(
            f'Message de {user_name} depuis le site web',
            formatted_message,                
            user_email,
            ['lekamyangambibenido@gmail.com'],
        )

        return redirect('home')
    return render(request, 'contact.html')


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'blog/articles_list.html', {'articles': articles})


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    commentaires = article.commentaires.all().prefetch_related('reponses')

    form = CommentaireForm()
    reponse_form = ReponseForm()

    if request.method == 'POST' and request.user.is_authenticated:
        if 'commentaire_form' in request.POST:
            form = CommentaireForm(request.POST)
            if form.is_valid():
                commentaire = form.save(commit=False)
                commentaire.article = article
                commentaire.auteur = request.user
                commentaire.save()
                messages.success(request, "Votre commentaire a été ajouté avec succès.")
                return redirect('article_detail', slug=article.slug)
            else:
                messages.error(request, "Erreur dans le formulaire de commentaire.")
        elif 'reponse_form' in request.POST:
            reponse_form = ReponseForm(request.POST)
            if reponse_form.is_valid():
                reponse = reponse_form.save(commit=False)
                commentaire_id = request.POST.get('commentaire_id')
                commentaire = get_object_or_404(Commentaire, id=commentaire_id)
                reponse.commentaire = commentaire
                reponse.auteur = request.user
                reponse.save()
                messages.success(request, "Votre réponse a été ajoutée avec succès.")
                return redirect('article_detail', slug=article.slug)
            else:
                messages.error(request, "Erreur dans le formulaire de réponse.")

    return render(request, 'blog/article_detail.html', {
        'article': article,
        'commentaires': commentaires,
        'form': form,
        'reponse_form': reponse_form
    })


@login_required
@admin_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                article = form.save(commit=False)
                article.auteur = request.user
                article.save()
                messages.success(request, 'Article créé avec succès!')
                return redirect('article_detail', slug=article.slug)
            except ValidationError as e:
                messages.error(request, str(e))
                return render(request, 'blog/article_form.html', {'form': form})
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})


@login_required
@admin_required
def article_update(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            try:
                article = form.save()
                messages.success(request, 'Article mis à jour avec succès!')
                return redirect('article_detail', slug=article.slug)
            except ValidationError as e:
                messages.error(request, str(e))
                return render(request, 'blog/article_form.html', {'form': form})
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_form.html', {'form': form})


@login_required
@admin_required
def article_delete(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article supprimé avec succès!')
        return redirect('article_list')
    return render(request, 'blog/article_confirm_delete.html', {'article': article})


@login_required
def like_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': article.total_likes()
    })


@login_required
def commentaire_delete(request, id):
    commentaire = get_object_or_404(Commentaire, id=id)
    if request.user == commentaire.article.auteur:
        commentaire.delete()
        messages.success(request, 'Commentaire supprimé avec succès!')
    return redirect('article_detail', slug=commentaire.article.slug)


@login_required
def like_commentaire(request, commentaire_id):
    commentaire = get_object_or_404(Commentaire, id=commentaire_id)

    # Vérifie si l'utilisateur a déjà aimé le commentaire
    if commentaire.likes.filter(id=request.user.id).exists():
        commentaire.likes.remove(request.user)
        liked = False
    else:
        commentaire.likes.add(request.user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': commentaire.total_likes()
    })


@login_required
def ajouter_reponse(request, commentaire_id):
    commentaire = get_object_or_404(Commentaire, id=commentaire_id)
    if request.method == 'POST':
        form = ReponseForm(request.POST)
        if form.is_valid():
            reponse = form.save(commit=False)
            reponse.auteur = request.user
            reponse.commentaire = commentaire
            reponse.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Méthode non autorisée'})
