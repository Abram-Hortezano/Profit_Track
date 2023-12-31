# pages/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import PasswordsChangeView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.signin, name='signin'),
    path("signin", views.signin, name='signin'),
    path("register", views.register, name='register'),
    path("index", views.index, name='index'),
    path("profile", views.profile, name='profile'),
    path("about", views.about, name='about'),

    #passwordchange
    #path("password", auth_views.PasswordChangeView.as_view(template_name='pages/change-password.html')),
    path("password", PasswordsChangeView.as_view(template_name='pages/change-password.html')),
    path("password_success", views.password_success, name = "password_success"),
    path("recordtransaction", views.recordtransaction, name = "recordtransaction"),
    path("updateprofile", views.updateprofile, name = "updateprofile"),
    path("delete_transaction/<int:transaction_id>/", views.delete_transaction, name="delete-transaction"),
    path("search", views.search, name="search"),
    path("goals", views.goals, name='goals'),
    path("create_goal", views.create_goal, name='create_goal'),
    path("update_goal/<int:goal_id>", views.update_goal, name='update_goal'),
    path("delete_goal/<int:goal_id>", views.delete_goal, name='delete_goal'),
    path('transaction_graph', views.transaction_graph, name='transaction_graph'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)