
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserProfileForm
import logging
from .models import User

logger = logging.getLogger(__name__)  # Initializare logger

def user_login(request):
    logger.info("Intrat în user_login")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        logger.info(f"Username introdus: {username}")
        logger.info(f"Parola introdusă: {password}")
        try:
            user_from_db = User.objects.get(username=username)
            logger.info(f"Utilizator din baza de date: {user_from_db}")
        except User.DoesNotExist:
            logger.warning("Utilizatorul nu există în baza de date")
            user_from_db = None

        user = authenticate(request, username=username, password=password)
        logger.info(f"Utilizator autentificat: {user}")
        if user is not None:
            login(request, user)
            logger.info("Autentificare reușită")
            messages.success(request, 'Autentificare reușită!')
            return redirect('welcome')
        else:
            logger.warning("Autentificare eșuată")
            messages.error(request, 'Nume de utilizator sau parolă incorecte.')
    return render(request, 'users/login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  # Nu salva utilizatorul imediat
            user.set_password(form.cleaned_data['password'])  # Hash-ează parola
            user.save()  # Salvează utilizatorul cu parola hash-ată
            if user:
                login(request, user)
                messages.success(request, 'Contul a fost creat cu succes!')
                return redirect('welcome')
            else:
                messages.error(request, 'A apărut o eroare la crearea contului.')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)  # Important: request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilul a fost actualizat cu succes!')
            return redirect('profile')
        else:
            messages.error(request, 'A apărut o eroare la actualizarea profilului.')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})