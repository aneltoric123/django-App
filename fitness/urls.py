from django.urls import path

from . import views

urlpatterns = [
    path('',views.login_page,name='login'),
    path('home/',views.home_page,name='home_page'),
    path('complete_profile/',views.complete_profile,name = 'complete_profile'),
    path('register/',views.register_page,name='register'),
    path('logout/',views.logout_page,name='logout'),
    path('profile/',views.profile_page,name='profile'),
    path('profle/edit',views.edit_profile,name='edit_profile'),
    path('profile/delete',views.delete_profile,name='delete_profile'),
    path('home/delete_weight_record/<int:record_id>/',views.delete_weight_record,name='delete_weight_record')
]