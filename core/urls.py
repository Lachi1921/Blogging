from django.urls import path
from .views import *


app_name = "core"

urlpatterns = [
    path('', homepage, name="homepage"),
    path('signup/', register_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='reset_password'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # posts
    path('post/create/', post_create_view, name='post_create'),
    path('post/<slug:slug>/edit/', post_edit, name='post_edit'),
    path('post/<slug:slug>/delete/', post_delete, name='post_delete'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('category/<str:category_slug>/', category_posts, name='category-posts'),
    path('tag/<str:tag_slug>/', tag_posts, name='tag-posts'),

    #user
    path('user/@<str:username>/', profile_view, name='profile'),
    path('user/@<str:username>/edit/', settings, name='settings'),
    path('search/', search, name='search'),

]

