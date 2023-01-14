from django.urls import path
from .views import (
    AgentListView, AgentCreateView, AgentDetailView, 
    AgentUpdateView, AgentDeleteView,RecepieListView,CreateRecepie
)
from leads.views import (
    LeadListView,TransactionsLeadListView,TransactionListView,TransactionCreateView)
app_name = 'agents'

urlpatterns = [
    path('', AgentListView.as_view(), name='agent-list'),
    path('<int:pk>/', AgentDetailView.as_view(), name='agent-detail'),
    path('<int:pk>/create-recepie/', CreateRecepie, name='create-recepie'),
    path('<int:pk>/update/', AgentUpdateView.as_view(), name='agent-update'),
    path('<int:pk>/delete/', AgentDeleteView.as_view(), name='agent-delete'),
    path('create/', AgentCreateView.as_view(), name='agent-create'),
    path('<int:pk>/transactions/', TransactionListView.as_view(), name='agent-transactions-list'),
    path('<int:pk>/recepie/', RecepieListView.as_view(), name='agent-lead-list-nontransactions'),
    #  path('<int:pk>/pdf/', ViewPDF.as_view(), name='agent-lead-list-nontransactions'),
    # path('<int:pk>/nontransactions/', TransactionsLeadListView.as_view(), name='agent-lead-list-nontransactions'),
    path('<int:pk>/leads/', LeadListView.as_view(), name='agent-leads-list'),
    path('<int:pk>/transactions/create/', TransactionCreateView.as_view(), name='agent-transactions-create'),
]