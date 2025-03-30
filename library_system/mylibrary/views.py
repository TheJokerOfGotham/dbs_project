from django.shortcuts import render, HttpResponse, redirect
from .forms import MemberRegistrationForm
from .models import Member



# Create your views here.

def entry(request):
    return render(request, "entry.html")

def register_member(request):
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('/')  # Redirect to a member list page after registration
    else:
        form = MemberRegistrationForm()

    return render(request, 'register_member.html', {'form': form})

def search_member(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    members = Member.objects.filter(name__icontains=query) if query else Member.objects.all()

    return render(request, 'search_member.html', {'members': members, 'query': query})