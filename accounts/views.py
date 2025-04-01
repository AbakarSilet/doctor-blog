from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EditUserProfileForm, SignUpForm, LoginForm, UserProfileForm
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from .forms import CustomPasswordResetForm, CustomSetPasswordForm
from .models import User

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie!')
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Connexion réussie!')
                # Rediriger vers la page précédente si elle existe
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('home')
            else:
                messages.error(request, 'Email ou mot de passe invalide.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Déconnexion réussie!')
    return redirect('home')

@login_required
def profile_view(request):
    user = request.user
    form = UserProfileForm(instance=user)
    return render(request, 'accounts/profile.html', {'form': form, 'user': user})

@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = EditUserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = EditUserProfileForm(instance=user)
    return render(request, 'accounts/edit_profile.html', {'form': form})





# Configuration du logger
logger = logging.getLogger(__name__)

def password_reset_request(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
                
                # Génération du token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Construction du lien de réinitialisation
                current_site = get_current_site(request)
                reset_url = request.build_absolute_uri(
                    reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                
                # Préparation du contenu des emails (texte et HTML)
                context = {
                    'user': user,
                    'reset_url': reset_url,
                    'site_name': current_site.name,
                }
                
                subject = "Réinitialisation de votre mot de passe"
                text_content = render_to_string('accounts/password_reset_email.txt', context)
                html_content = render_to_string('accounts/password_reset_email.html', context)
                
                # Création et envoi de l'email
                try:
                    email_msg = EmailMultiAlternatives(
                        subject, 
                        text_content, 
                        settings.DEFAULT_FROM_EMAIL, 
                        [user.email]
                    )
                    email_msg.attach_alternative(html_content, "text/html")
                    email_sent = email_msg.send(fail_silently=False)
                    
                    if email_sent:
                        messages.success(
                            request, 
                            f"Un email de réinitialisation a été envoyé à {email}. "
                            f"Veuillez vérifier votre boîte de réception et éventuellement vos spams."
                        )
                    else:
                        logger.error(f"Échec d'envoi d'email à {email}")
                        messages.error(
                            request, 
                            "Un problème est survenu lors de l'envoi du mail. Veuillez contacter l'administrateur."
                        )
                        
                except Exception as e:
                    logger.error(f"Erreur d'envoi d'email: {str(e)}")
                    messages.error(
                        request, 
                        "Un problème technique empêche l'envoi d'email. Veuillez réessayer plus tard ou contacter l'administrateur."
                    )
                
                # Rediriger même si l'email échoue pour des raisons de sécurité
                return redirect('accounts:login')
                
            except User.DoesNotExist:
                # Ne pas révéler si un utilisateur existe ou non
                messages.success(
                    request, 
                    "Si cette adresse email est associée à un compte, un email de réinitialisation a été envoyé."
                )
                return redirect('accounts:login')
    else:
        form = CustomPasswordResetForm()
    
    return render(request, 'accounts/password_reset_form.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    # Vérification du token
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Votre mot de passe a été réinitialisé avec succès. Vous pouvez maintenant vous connecter.")
                return redirect('accounts:login')
        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Le lien de réinitialisation est invalide ou a expiré.")
        return redirect('accounts/password_reset_request')
    
    