from django.shortcuts import render,redirect,HttpResponse
from users.forms import CustomRegistrationForm,LoginForm,CreateGroupForm
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from events.models import Event,Category
from django.db.models import Q, Count
from django.utils import timezone

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists() or user.is_superuser

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            user_group, created = Group.objects.get_or_create(name='User')
            user.groups.add(user_group)
            messages.success(
                request, 'A Confirmation mail sent. Please check your email')
            return redirect('sign-in')

    return render(request, 'registration/register.html', {"form": form})


def sign_in(request):
    form = LoginForm()

    if request.method == 'POST' :
        form = LoginForm(request,data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    return render(request,'registration/login.html',{'form':form})    

@login_required
def sign_out(request):
        logout(request)
        return redirect('sign-in')
    

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')





@user_passes_test(is_admin)
def admin_dashboard(request):

    total_participants = User.objects.exclude(is_superuser=True).count()
    total_events = Event.objects.count()
    total_groups = Group.objects.count()
    total_categories = Category.objects.count()

    
    filter_type = request.GET.get('view', 'events') 
    items = []
    list_title = ""

    if filter_type == 'events':
        list_title = "All System Events"
        
        items = Event.objects.select_related('category').annotate(
            participant_count=Count('participants')
        ).all().order_by('-date')

    elif filter_type == 'groups':
        list_title = "User Groups & Permissions"
       
        items = Group.objects.all().annotate(
            user_count=Count('user')
        )

    elif filter_type == 'categories':
        list_title = "Event Categories"
     
        items = Category.objects.all().annotate(
            event_count=Count('events')
        )

    elif filter_type == 'participants':
        list_title = "All Registered Users"
        
        items = User.objects.exclude(is_superuser=True).prefetch_related('groups').only(
            'username', 'email'
        )

    context = {
        'total_events': total_events,
        'total_participants': total_participants,
        'total_groups': total_groups,
        'total_categories': total_categories,
        'items': items,
        'filter_type': filter_type,
        'list_title': list_title,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)


@user_passes_test(is_admin)
def delete_participant(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)

        if not user.is_superuser: 
            user.delete()
            messages.success(request, "User deleted successfully.")

    return redirect('admin-dashboard')


@user_passes_test(is_admin)
def assign_role(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        group_name = request.POST.get('role')
        group = Group.objects.get(name=group_name)
    
        user.groups.clear() 
        user.groups.add(group)

        messages.success(request, f"Assigned {user.username} to {group_name}")
    return redirect('admin-dashboard')

@user_passes_test(is_admin)
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect('admin-dashboard')

    return render(request, '/users/admin-dashboard/?view=groups', {'form': form})

@user_passes_test(is_admin)
def delete_group(request, group_id):
    if request.method == 'POST':
        group = Group.objects.get(id=group_id)
        group_name = group.name
        group.delete()
        messages.success(request, f"Role '{group_name}' has been deleted.")
    return redirect('/users/admin-dashboard/?view=groups')

@user_passes_test(is_admin)
def delete_category(request, category_id):
    if request.method == 'POST':
        category = Category.objects.get( id=category_id)
        cat_name = category.name
        category.delete()
        messages.success(request, f"Category '{cat_name}' has been deleted.")
    return redirect('/users/admin-dashboard/?view=categories')


@login_required
def participant_dashboard(request):
    my_rsvps = request.user.attended_events.all().select_related('category')
    
    return render(request, 'dashboard/participant_dashboard.html', {
        'events': my_rsvps
    })