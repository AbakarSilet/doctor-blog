from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('article/new/', views.article_create, name='article_create'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('article/<slug:slug>/edit/', views.article_update, name='article_update'),
    path('article/<slug:slug>/delete/', views.article_delete, name='article_delete'),
    path('commentaire/<int:id>/delete/', views.commentaire_delete, name='commentaire_delete'),
    path('article/<slug:slug>/like/', views.like_article, name='like_article'),
    path('like_commentaire/<int:commentaire_id>/', views.like_commentaire, name='like_commentaire'),
    path('ajouter_reponse/<int:commentaire_id>/', views.ajouter_reponse, name='ajouter_reponse'),

    path('404',views.custom_404,name='404'),
    path('403',views.custom_403,name='403'),
    path('transition/', views.transition_page, name='transition_page'),
    path('contact/', views.contact, name='contact_us'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('about/', views.about, name='about_us'),
    path('send_email/',views.send_email,name='send_email'),
]