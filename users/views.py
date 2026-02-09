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
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView,CreateView,DeleteView


def is_organizer(user):
    return user.groups.filter(name='Organizer').exists() or user.is_superuser

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

# def sign_up(request):
#     form = CustomRegistrationForm()
#     if request.method == 'POST':
#         form = CustomRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data.get('password1'))
#             user.is_active = False
#             user.save()
#             user_group, created = Group.objects.get_or_create(name='User')
#             user.groups.add(user_group)
#             messages.success(
#                 request, 'A Confirmation mail sent. Please check your email')
#             return redirect('sign-in')

#     return render(request, 'registration/register.html', {"form": form})

class SignUp(FormView):
    form_class = CustomRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password1'))
        user.is_active = False
        user.save()

        messages.success(
            self.request,
            'A confirmation mail has been sent. Please check your email.'
        )
        return super().form_valid(form)
    

# def sign_in(request):
#     form = LoginForm()

#     if request.method == 'POST' :
#         form = LoginForm(request,data = request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request,user)
#             return redirect('home')
#     return render(request,'registration/login.html',{'form':form})    


class CustomLoginView(LoginView):
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()
    

# @login_required
# def sign_out(request):
#         logout(request)
#         return redirect('sign-in')

    

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





# @user_passes_test(is_admin)
# def admin_dashboard(request):

#     total_participants = User.objects.exclude(is_superuser=True).count()
#     total_events = Event.objects.count()
#     total_groups = Group.objects.count()
#     total_categories = Category.objects.count()

    
#     filter_type = request.GET.get('view', 'events') 
#     items = []
#     list_title = ""

#     if filter_type == 'events':
#         list_title = "All System Events"
        
#         items = Event.objects.select_related('category').annotate(
#             participant_count=Count('participants')
#         ).all().order_by('-date')

#     elif filter_type == 'groups':
#         list_title = "User Groups & Permissions"
       
#         items = Group.objects.all().annotate(
#             user_count=Count('user')
#         )

#     elif filter_type == 'categories':
#         list_title = "Event Categories"
     
#         items = Category.objects.all().annotate(
#             event_count=Count('events')
#         )

#     elif filter_type == 'participants':
#         list_title = "All Registered Users"
        
#         items = User.objects.exclude(is_superuser=True).prefetch_related('groups').only(
#             'username', 'email'
#         )

#     context = {
#         'total_events': total_events,
#         'total_participants': total_participants,
#         'total_groups': total_groups,
#         'total_categories': total_categories,
#         'items': items,
#         'filter_type': filter_type,
#         'list_title': list_title,
#     }

#     return render(request, 'dashboard/admin_dashboard.html', context)

@method_decorator(user_passes_test(is_admin),name='dispatch')
class AdminDashboard(TemplateView):
    template_name = 'dashboard/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Stats
        context['total_participants'] = User.objects.exclude(is_superuser=True).count()
        context['total_events'] = Event.objects.count()
        context['total_groups'] = Group.objects.count()
        context['total_categories'] = Category.objects.count()

        filter_type = self.request.GET.get('view', 'events')
        context['filter_type'] = filter_type

        if filter_type == 'events':
            context['list_title'] = "All System Events"
            context['items'] = (
                Event.objects
                .select_related('category')
                .annotate(participant_count=Count('participants'))
                .order_by('-date')
            )

        elif filter_type == 'groups':
            context['list_title'] = "User Groups & Permissions"
            context['items'] = (
                Group.objects
                .annotate(user_count=Count('user'))
            )

        elif filter_type == 'categories':
            context['list_title'] = "Event Categories"
            context['items'] = (
                Category.objects
                .annotate(event_count=Count('events'))
            )

        elif filter_type == 'participants':
            context['list_title'] = "All Registered Users"
            context['items'] = (
                User.objects
                .exclude(is_superuser=True)
                .prefetch_related('groups')
                .only('username', 'email')
            )

        else:
            context['list_title'] = ""
            context['items'] = []

        return context


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

# @user_passes_test(is_admin)
# def create_group(request):
#     form = CreateGroupForm()
#     if request.method == 'POST':
#         form = CreateGroupForm(request.POST)

#         if form.is_valid():
#             group = form.save()
#             messages.success(request, f"Group {group.name} has been created successfully")
#             return redirect('dashboard/?view=groups')
    
#     return render(request, 'dashboard/create_group.html',{'form':form})

@method_decorator(user_passes_test(is_admin),name= 'dispatch')
class CreateGroup(CreateView):
    model = Group
    form_class = CreateGroupForm 
    template_name = 'dashboard/create_group.html'
    success_url = '/users/admin-dashboard/?view=groups'

    def form_valid(self, form):
        group = form.save()
        messages.success(
            self.request,
            f"Group '{group.name}' has been created successfully"
        )
        return super().form_valid(form)
    
    
 

    

# @user_passes_test(is_admin)
# def delete_group(request, group_id):
#     if request.method == 'POST':
#         group = Group.objects.get(id=group_id)
#         group_name = group.name
#         group.delete()
#         messages.success(request, f"Role '{group_name}' has been deleted.")
#     return redirect('/users/admin-dashboard/?view=groups')

@method_decorator(user_passes_test(is_admin),name='dispatch')
class DeleteGroup(DeleteView):
    model = Group
    pk_url_kwarg = 'group_id'
    success_url = '/users/admin-dashboard/?view=groups'


# @user_passes_test(is_admin)
# def delete_category(request, category_id):
#     if request.method == 'POST':
#         category = Category.objects.get( id=category_id)
#         cat_name = category.name
#         category.delete()
#         messages.success(request, f"Category '{cat_name}' has been deleted.")
#     return redirect('/users/admin-dashboard/?view=categories')

@method_decorator(user_passes_test(is_admin),name='dispatch')
class DeleteCategory(DeleteView):
    model = Category
    pk_url_kwarg = 'category_id'
    success_url = '/users/admin-dashboard/?view=categories'



@login_required
def participant_dashboard(request):
    my_rsvps = request.user.attended_events.all().select_related('category')
    
    return render(request, 'dashboard/participant_dashboard.html', {
        'events': my_rsvps
    })