from django.contrib import admin
from django.urls import path
from users.views import SignUp,CustomLoginView,ChangePassword,AdminDashboard,EditProfileView,CustomPasswordResetConfirmView,CustomPasswordResetView,ProfileView,CreateGroup,DeleteGroup,DeleteCategory,activate_user,participant_dashboard,delete_participant,assign_role
#sign_up,sign_in,sign_out,admin_dashboard,create_group,delete_group,delete_category
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeDoneView
urlpatterns = [

    path('admin/', admin.site.urls),
    # path('sign-up/',sign_up,name = 'sign-up'),
    path('sign-up/',SignUp.as_view(),name = 'sign-up'),
    #path('sign-in/',sign_in,name = 'sign-in'),
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    # path('sign-out/',sign_out,name = 'logout'),
    path('sign-out/',LogoutView.as_view(),name = 'logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    #path('admin-dashboard/',admin_dashboard,name='admin-dashboard'),
    path('admin-dashboard/',AdminDashboard.as_view(),name='admin-dashboard'),
    path('assign-role/<int:user_id>/', assign_role, name='assign-role'),
    path('delete-participant/<int:user_id>/', delete_participant, name='delete-participant'),
    #path('admin-dashboard/create-group/', create_group, name='create-group'),
    path('admin-dashboard/create-group/',CreateGroup.as_view(), name='create-group'),
    # path('admin-dashboard/delete-group/<int:group_id>/', delete_group, name='delete-group'),
    path('admin-dashboard/delete-group/<int:group_id>/', DeleteGroup.as_view(), name='delete-group'),
    #path('admin-dashboard/delete-category/<int:category_id>/',delete_category, name='delete-category'),
    path('admin-dashboard/delete-category/<int:category_id>/',DeleteCategory.as_view(), name='delete-category'),
    path('my-dashboard/',participant_dashboard, name='participant-dashboard'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('edit-profile/',EditProfileView.as_view(),name='edit_profile'),
    path('password-change/',ChangePassword.as_view(),name = 'password_change'),
    path('password-change-done/',PasswordChangeDoneView.as_view(template_name = 'accounts/password_change_done.html'),name = 'password_change_done'),
    path('password-reset/',CustomPasswordResetView.as_view(),name = 'password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(),name = 'password_reset_confirm'),
]
    