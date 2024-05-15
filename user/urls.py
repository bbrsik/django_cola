from django.urls import path, include
from . import views, api_views

urlpatterns = [
    path('login/', views.render_login, name='render_login'),
    path('signup/', views.render_signup, name='render_signup'),
    path('profile/', views.render_edit_profile, name='render_profile'),

    path('api/', include([
        path('login/', api_views.login_view, name='login_view'),
        path('logout/', api_views.logout_view, name='logout_view'),
        path('create_user/', api_views.create_user, name='create_user'),
        path('edit_profile/', api_views.edit_profile, name='edit_profile'),
        path('display_profile/', api_views.display_profile, name='display_profile'),
    ])),
]
