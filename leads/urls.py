
from django.urls import path
# from .views import (
#     LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView,
#     AssignAgentView,
#      LeadJsonView, 
#     FollowUpCreateView, FollowUpUpdateView, FollowUpDeleteView
# )

from .views import * #lead_list ,lead_update , lead_delete , lead_detail
# app_name = "leads"

urlpatterns = [
    # path('', LeadListView.as_view(), name='lead-list'),
    # path('status__exact=<str:status>/', LeadListView.as_view(), name='lead-list'),
    # path('today/', TodayLeadListView.as_view(), name='lead-list-today'),
    # path('today/?status__exact=<str:status>/', TodayLeadListView.as_view(), name='lead-list-today'),
    # path('nontransactions/', TransactionsLeadListView.as_view(), name='lead-list-nontransactions'),
    # # path('json/', LeadJsonView.as_view(), name='lead-list-json'),
    # path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    # path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    # path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    # path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    # # path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    # path('<int:pk>/followups/create/', FollowUpCreateView.as_view(), name='lead-followup-create'),
    # path('followups/<int:pk>/', FollowUpUpdateView.as_view(), name='lead-followup-update'),
    # path('followups/<int:pk>/delete/', FollowUpDeleteView.as_view(), name='lead-followup-delete'),
    # path('create/', LeadCreateView.as_view(), name='lead-create'),
    # path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    # path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    # path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='cate/gory-delete'),
    # path('create-category/', CategoryCreateView.as_view(), name='category-create'),
]