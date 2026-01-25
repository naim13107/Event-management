from django.contrib import admin
from django.urls import path
from users.views import sign_up,sign_in,sign_out,activate_user,participant_dashboard,delete_group,delete_category,admin_dashboard,create_group,delete_participant,assign_role

urlpatterns = [

    path('admin/', admin.site.urls),
    path('sign-up/',sign_up,name = 'sign-up'),
    path('sign-in/',sign_in,name = 'sign-in'),
    path('sign-out/',sign_out,name = 'logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin-dashboard/',admin_dashboard,name='admin-dashboard'),
    path('assign-role/<int:user_id>/', assign_role, name='assign-role'),
    path('delete-participant/<int:user_id>/', delete_participant, name='delete-participant'),
    path('admin-dashboard/create-group/', create_group, name='create-group'),
    path('admin-dashboard/delete-group/<int:group_id>/', delete_group, name='delete-group'),
    path('admin-dashboard/delete-category/<int:category_id>/',delete_category, name='delete-category'),
    path('my-dashboard/',participant_dashboard, name='participant-dashboard'),
]
    