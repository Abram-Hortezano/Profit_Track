import re
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Goal, Profile, PaymentMethod, Category , RecordTransaction
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from .forms import GoalForm, SignUpForm, ProfilePicForm, RecordTransactionForm
from django import forms
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import F, Value
from django.db.models.functions import Concat
from reportlab.pdfgen import canvas
from django.shortcuts import render
from django.http import HttpResponse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from .models import Goal


def transaction_graph(request):
    transactions = RecordTransaction.objects.all()

    dates = [transaction.transaction_date for transaction in transactions]
    amounts = [transaction.transaction_amount for transaction in transactions]

    # Determine if each transaction is increasing or decreasing
    colors = ['green' if amounts[i] <= amounts[i+1] else 'red' for i in range(len(amounts)-1)]
    colors.append('green')  # Set color for the last point

    # Create a line chart with different colors for each line segment
    plt.figure(figsize=(14, 6))

    for i in range(len(dates)-1):
        plt.plot(dates[i:i+2], amounts[i:i+2], marker='o', linestyle='-', color=colors[i])
        plt.annotate(f'{amounts[i]:.2f}', (dates[i], amounts[i]), textcoords="offset points", xytext=(0,10), ha='center')

    # Add annotation for the last point
    plt.annotate(f'{amounts[-1]:.2f}', (dates[-1], amounts[-1]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.title('Transaction Amounts Over Time (Line Chart)')
    plt.xlabel('Transaction Date')
    plt.ylabel('Transaction Amount')
    plt.grid()

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', bbox_inches='tight')
    plt.close()

    # Convert the BytesIO object to a base64 encoded string
    image_stream.seek(0)
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')

    # Create a data URI for the HTML img tag
    image_data_uri = f'data:image/png;base64,{encoded_image}'

    # Pass the image data URI to the template
    context = {'image_data_uri': image_data_uri}

    return render(request, 'pages/transaction_graph.html', context)





@login_required(login_url='signin')
def goals(request):
    user_goals = Goal.objects.filter(user=request.user)
    return render(request, 'pages/goals.html', {'user_goals': user_goals})

@login_required(login_url='signin')
def create_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, "Goal created successfully!")
            return redirect('goals')
    else:
        form = GoalForm()

    return render(request, 'pages/create_goal.html', {'form': form})

@login_required(login_url='signin')
def update_goal(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)

    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, "Goal updated successfully!")
            return redirect('goals')
    else:
        form = GoalForm(instance=goal)

    return render(request, 'pages/update_goal.html', {'form': form, 'goal': goal})

@login_required(login_url='signin')
def delete_goal(request, goal_id):
    goal = Goal.objects.get(pk=goal_id)
    goal.delete()
    messages.success(request, "Goal deleted successfully!")
    return redirect('goals')

@login_required(login_url='signin')
def index(request):
    username = request.user.username
    return render(request, "pages/index.html", {'username': username } )

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
    if request.method == 'POST':
        form = RecordTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Successfully Created")
            return redirect('recordtransaction')  # Redirect to the same page
    else:
        form = RecordTransactionForm()

    all_items = RecordTransaction.objects.all()
    return render(request, 'pages/recordtransaction.html', {'form': form, 'all': all_items})

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
        search_term = request.POST.get('searched', '').strip()
        if search_term:
            search_terms = search_term.split()  # Split the search term by spaces
            transactions = RecordTransaction.objects.all()

            for term in search_terms:
                transactions = transactions.filter(
                    Q(customer_name__icontains=term) |
                    Q(category__name__iexact=term) |
                    Q(payment_method__name__iexact=term) |
                    Q(transaction_id__iexact=term)
                )

            return render(request, 'pages/search.html', {'searched': search_term, 'transactions': transactions})
        else:
            return render(request, 'pages/search.html', {'searched': search_term, 'error_message': 'Please enter a search term'})
    else:
        return render(request, 'pages/search.html')

def search_goals(request):
    search_term = request.GET.get('search', '')
    user_goals = Goal.objects.filter(description__icontains=search_term)

    context = {
        'user_goals': user_goals,
    }
    return render(request, 'pages/goals.html', context)
