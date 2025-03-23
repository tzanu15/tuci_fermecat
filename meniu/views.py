from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .forms import DishForm
from .models import Dish, Vote
from django.contrib import messages
import datetime

@login_required
def vote_dish(request):
    """
    Handles user voting for a dish.
    """
    if request.method == 'POST':
        dish_id = request.POST.get('dish_id')
        dish = get_object_or_404(Dish, id=dish_id)

        try:
            Vote.objects.create(user=request.user, dish=dish)
            messages.success(request, 'Vote registered successfully!')
            return JsonResponse({'status': 'success'})
        except:
            messages.error(request, 'You have already voted for this dish.')
            return JsonResponse({'status': 'error', 'message': 'You have already voted for this dish.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed.'})

def dish_list(request):
    dishes = Dish.objects.all()  # Obține toate preparatele din baza de date
    return render(request, 'meniu/dish_list.html', {'dishes': dishes})

@login_required
def add_dish(request):
    """
    Adds a new dish (only for admin users).
    """
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to add dishes.")
        return redirect('dish_list')  # Redirect to dish list or another appropriate page

    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            dish = form.save(commit=False)
            dish.author = request.user
            dish.save()
            messages.success(request, 'Dish added successfully!')
            return redirect('dish_list')
        else:
            messages.error(request, 'Error adding dish.')
    else:
        form = DishForm()
    return render(request, 'meniu/add_dish.html', {'form': form})



def winning_dish(request):
    """
    Displays the winning dish at the end of the voting period (Friday).
    """
    today = datetime.datetime.now().weekday()
    if today == 4:  # 4 = Friday
        dishes = Dish.objects.all()
        winner = None
        max_votes = 0
        for dish in dishes:
            vote_count = dish.vote_count()
            if vote_count > max_votes:
                max_votes = vote_count
                winner = dish
        return render(request, 'meniu/winning_dish.html', {'winner': winner})
    else:
        return render(request, 'meniu/winning_dish.html', {'winner': None})  # Or redirect to dish list