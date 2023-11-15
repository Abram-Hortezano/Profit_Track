import re
from django.shortcuts import redirect, render, HttpResponse,HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, PaymentMethod, Category , RecordTransaction, FinancialGoal
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from .forms import SignUpForm, ProfilePicForm, RecordTransactionForm, FinancialGoalForm
from django import forms
from django.http import JsonResponse
from django.db.models import Q

@login_required(login_url='signin')
def index(request):
    username = request.user.username
    goals = FinancialGoal.objects.filter(user=request.user)
    return render(request, "pages/index.html", {'username': username, 'goals': goals } )

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('index')

        else:
            messages.error(request, "Invalid Credentials")

    return render(request, "pages/signin.html")

# ...

def register(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        # Define a regex pattern to allow only alphanumeric characters
        pattern = r'^[a-zA-Z0-9]+$'

        if pass1 == pass2:
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
            elif not re.match(pattern, username):
                messages.error(request, "Username can only contain letters and numbers")
            elif len(username) < 5:
                messages.error(request, "Username must be at least 5 characters")
            elif len(pass1) < 5:
                messages.error(request, "Password must be at least 5 characters")
            else:
                myuser = User.objects.create_user(username, email, pass1)
                myuser.save()
                messages.success(request, "Account Successfully Created")
                return redirect('signin')
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "pages/register.html")

def profile(request):
    # Your view logic here
    return render(request, 'pages/profile.html')

# Create your views here.
def about(request):
    # Your view logic here
    return render(request, 'pages/about.html')

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request, 'pages/password_success.html')
def recordtransaction(request):
    all_items = RecordTransaction.objects.all
    if request.method == 'POST':
        form = RecordTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(recordtransaction)  
    else:
        form = RecordTransactionForm()
    
    return render(request, 'pages/recordtransaction.html', {'form': form,'all':all_items})

def delete_transaction(request, transaction_id):
    try:
        transaction = RecordTransaction.objects.get(transaction_id=transaction_id)
        transaction.delete()
        return JsonResponse({'message': 'Transaction deleted successfully'})
    except RecordTransaction.DoesNotExist:
        return JsonResponse({'message': 'Transaction not found'}, status=404)

def updateprofile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)

        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, ("Your Profile Has Been Updated!"))
            return redirect('profile')
        return render(request, "pages/updateprofile.html", {'user_form':user_form, 'profile_form':profile_form})
    else: 
        messages.success(request, ("You Must Be Logged In to View That Page..."))
        return redirect('home')

def search(request):   
    if request.method == 'POST':
        searched = request.POST['searched']
        transaction = RecordTransaction.objects.filter(Q(transaction_id__contains=searched)|Q(customer_name__contains=searched)
                                                       |Q(contact_number__contains=searched)|Q(transaction_amount__contains=searched)
                                                       |Q(transaction_date__contains=searched)|Q(payment_method__name__contains=searched)|Q(category__name__contains=searched)   )

        return render(request, 'pages/search.html', {'searched':searched,'transaction':transaction})
    else:
        return render(request, 'pages/search.html', {})
    
def add_goal(request):
    if request.method == 'POST':
        form = FinancialGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('index')  # Assuming you have a home view
    else:
        form = FinancialGoalForm()
    
    return render(request, 'pages/add_goal.html', {'form': form})

@login_required
def view_goal(request, goal_id):
    goal = get_object_or_404(FinancialGoal, pk=goal_id, user=request.user)
    return render(request, 'pages/view_goal.html', {'goal': goal})

@login_required
def edit_goal(request, goal_id):
    goal = get_object_or_404(FinancialGoal, pk=goal_id, user=request.user)

    if request.method == 'POST':
        form = FinancialGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FinancialGoalForm(instance=goal)

    return render(request, 'pages\edit_goal.html', {'form': form, 'goal': goal})