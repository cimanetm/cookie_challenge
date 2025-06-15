from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recipe, Vote
from .forms import VoteForm

# Create your views here.

def index(request):
    context = {
        "contest_name": "Great Cookie Challenge",
        "introduction": "Welcome to the Great Cookie Challenge! Share your cookie recipes, bake them, and vote for the best cookies. Bakers and voters unite to create a sweet experience!",
        "instructions": [
            "Bakers: Share your best cookie recipes and show off your baking skills.",
            "Voters: Bake the cookies, upload proof, and vote for your favorite recipe.",
            "Winners: The recipe with the most votes wins the contest!",
        ],
    }
    return render(request, "index.html", context)

def register(request):
    context = {
        "contest_name": "Great Cookie Challenge",
        "introduction": "Welcome to the Great Cookie Challenge! ONLINE REGISTRATION IS UNDER CONSTRUCTION.",
        "instructions": [
            "Bakers: Share your best cookie recipes and show off your baking skills.",
            "Voters: Bake the cookies, upload proof, and vote for your favorite recipe.",
        ],
    }
    return render(request, "index.html", context)

def vote(request):
    if request.method == "POST":
        form = VoteForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            username = form.cleaned_data.get("username")
            user = User.objects.get(username=username)
            vote = form.save(commit=False)
            vote.voter = user
            vote.save()
            messages.success(request, "Thank you for voting!")
            return redirect("index")
    else:
        form = VoteForm()

    recipes = Recipe.objects.all()
    context = {
        "form": form,
        "recipes": recipes,
    }
    return render(request, "vote.html", context)