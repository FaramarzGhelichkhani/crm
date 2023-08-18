from .views import OrderListView, OrderUpdateView, OrderProductBulkCreateView, OrderProductListView, OrderAcceptView, OrderStats
from django.urls import path, include
from .crm_views import *
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'', OrdertListView)
# router.register(r'recommendations', RecommendationOrdertListView.as_view())


app_name = "leads"
urlpatterns = [
    path('orders/', OrderListView.as_view({'get': 'list'}), name='order-list'),
    path('orders/recommendations/',
         OrderListView.as_view({'get': 'list'}), name='recom-order-list'),
    path('orders/ongoing/',
         OrderListView.as_view({'get': 'list'}), name='ongoing-order-list'),
    path('orders/stats/', OrderStats.as_view(), name='order-stat'),
    path('orders/<int:pk>/',
         OrderListView.as_view({'get': 'list'}), name='order'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:order_id>/accept/',
         OrderAcceptView.as_view(), name='order-accept'),

    path('orders/<int:order_id>/order_products/',
         OrderProductListView.as_view(), name='order-product-l'),
    path('orders/<int:order_id>/order_products/bulk/',
         OrderProductBulkCreateView.as_view(), name='order-product-bulk-create'),


    # crm
    path('', LeadListView.as_view(), name='lead-list'),
    path('status__exact=<str:status>/', LeadListView.as_view(), name='lead-list'),
    path('today/', TodayLeadListView.as_view(), name='lead-list-today'),
    path('today/?status__exact=<str:status>/',
         TodayLeadListView.as_view(), name='lead-list-today'),
    # path('nontransactions/', TransactionsLeadListView.as_view(), name='lead-list-nontransactions'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('<int:pk>/followups/create/',
         FollowUpCreateView.as_view(), name='lead-followup-create'),
    path('followups/<int:pk>/', FollowUpUpdateView.as_view(),
         name='lead-followup-update'),
    path('followups/<int:pk>/delete/',
         FollowUpDeleteView.as_view(), name='lead-followup-delete'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),

]
