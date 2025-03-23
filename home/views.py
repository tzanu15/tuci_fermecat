from django.shortcuts import render

def welcome(request):
    """
    View for the welcome page.
    """
    return render(request, 'home/welcome.html')