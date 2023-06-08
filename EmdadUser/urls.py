from django.urls import path
from .crm_views import (
    AgentListView, AgentCreateView, AgentDetailView, 
    AgentUpdateView, AgentDeleteView,RecepieListView,UserCreateView, MakeRecepieListView
)
from .views import validate_credentials, UserDetailView
from Order.crm_views import (
    LeadListView,TransactionListView,TransactionCreateView)
app_name = 'agents'

urlpatterns = [
    path('', AgentListView.as_view(), name='agent-list'),
    
    path('credentials/', validate_credentials, name='credential'),
    path('userinfo/', UserDetailView.as_view(), name='user-info'),
    
    path('<int:pk>/', AgentDetailView.as_view(), name='agent-detail'),
    # path('<int:pk>/create-recepie/', CreateRecepie, name='create-recepie'),
    path('<int:pk>/update/', AgentUpdateView.as_view(), name='agent-update'),
    path('<int:pk>/delete/', AgentDeleteView.as_view(), name='agent-delete'),
    path('create/', AgentCreateView.as_view(), name='agent-create'),
    path('create/user/', UserCreateView.as_view(), name='agent-user-create'),
    path('<int:pk>/transactions/', TransactionListView.as_view(), name='agent-transactions-list'),
    path('<int:pk>/makerecepiet/', MakeRecepieListView.as_view(), name='agent-lead-list-makerecipt'),
    path('<int:pk>/recepiet/?<int:gt>to<int:lt>/', RecepieListView.as_view(), name='agent-lead-list-transactions'),
    # path('<int:pk>/pdf/', ViewPDF.as_view(), name='agent-lead-list-nontransactions'),
    # path('<int:pk>/nontransactions/', TransactionsLeadListView.as_view(), name='agent-lead-list-nontransactions'),
    path('<int:pk>/leads/', LeadListView.as_view(), name='agent-leads-list'),
    path('<int:pk>/transactions/create/', TransactionCreateView.as_view(), name='agent-transactions-create'),
]