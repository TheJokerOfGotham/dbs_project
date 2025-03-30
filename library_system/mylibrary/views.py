from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, MemberForm
from .models import Member
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required




# Create your views here.

def entry(request):
    return render(request, "entry.html")




# def register_member(request):
#     if request.method == 'POST':
#         form = MemberRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()  # Save the form data to the database
#             return redirect('/')  # Redirect to a member list page after registration
#     else:
#         form = MemberRegistrationForm()

    # return render(request, 'register_member.html', {'form': form})

def search_member(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    members = Member.objects.filter(name__icontains=query) if query else Member.objects.all()

    return render(request, 'search_member.html', {'members': members, 'query': query})

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        member_form = MemberForm(request.POST)

        if user_form.is_valid() and member_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            member = member_form.save(commit=False)
            member.user = user  # Link Member with User
            member.email = user.email  # Sync email
            member.save()

            
            return redirect('login')  # Redirect after registration

    else:
        user_form = UserRegistrationForm()
        member_form = MemberForm()

    return render(request, "register.html", {"user_form": user_form, "member_form": member_form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")  # Redirect after login
    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {"form": form})

@login_required
def dashboard(request):
    member = request.user.member  # Get the Member object for the logged-in user
    response = render(request, "dashboard.html", {"member": member})
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response


def logout_view(request):
    logout(request)  # Logs out the user
    return redirect("login")  # Redirect to login page