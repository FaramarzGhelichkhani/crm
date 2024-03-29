from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# import django_sql_dashboard
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import path, include
from Order.crm_views import ( LandingPageView, DashboardView , TransactionListView, TransactionCreateView, TransactionUpdateView
 , TransactionDeleteView, SignupView )#landing_page

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginView(LoginView):
    authentication_form = AuthenticationForm

urlpatterns = [
    path('crm/motor/admin/', admin.site.urls),
    path('crm/motor/', LandingPageView.as_view(), name='landing-page'),
    path('crm/motor/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('crm/motor/leads/',  include('Order.urls', namespace="leads")),
    # path('crm/motor/Messeges/',  MessegesListView.as_view(), name="messeges-list"),
    path('crm/motor/agents/', include('EmdadUser.urls', namespace="agents")),
    path('crm/motor/emdad/',  include('Emdad.urls', namespace="emdad")),
    path('crm/motor/company/',  include('company.urls', namespace="company")),
    path('crm/motor/transactions/app/', include('Transaction.urls', namespace="transaction")),
    
    path('crm/motor/transactions/', TransactionListView.as_view(), name='transactions-list'),
    path('crm/motor/transactions/<int:pk>/', TransactionUpdateView.as_view(), name='transactions-update'),
    path('crm/motor/transactions/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transactions-delete'),
    path('crm/motor/signup/', SignupView.as_view(), name='signup'),
    path('crm/motor/reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('crm/motor/password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('crm/motor/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('crm/motor/password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('crm/motor/login/', LoginView.as_view(), name='login'),
    path('crm/motor/logout/', LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

