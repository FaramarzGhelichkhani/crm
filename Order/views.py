from .models import Order, Order_Product
from EmdadUser.models import Technecian
from Transaction.models  import Transaction
from .serializers import OrderSerializer, OrderProductSerializer, OrderProductListSerializer, OrderAcceptSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import permissions,status, viewsets, generics
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Avg, Sum, Q
from jalali_date import datetime2jalali





# class OrderListView(generics.ListAPIView,generics.UpdateAPIView,generics.RetrieveAPIView):
class OrderListView(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-time') 
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
        if self.request.get_full_path() == '/crm/motor/leads/orders/recommendations/':
            return self.queryset.filter(technecian=None,status="در آستانه کنسلی")
        elif self.request.get_full_path() == '/crm/motor/leads/orders/ongoing/':
            return self.queryset.filter(technecian__user_id=self.request.user, status='در حال انجام')
        elif  self.kwargs.get('pk') is None:
            return self.queryset.filter(technecian__user_id=self.request.user).exclude(status__in=['در حال انجام',"در آستانه کنسلی"])  

        else:  
            pk = int(self.kwargs['pk'])     
            return self.queryset.\
                filter(Q(id=pk) ).filter(technecian__user_id=self.request.user)   

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Update services field
        services_data = serializer.validated_data.get('services_list')
        if services_data:
            instance.services_list.set(services_data)

        # Update motors field
        motors_data = serializer.validated_data.get('motors')
        if motors_data:
            instance.motors.set(motors_data)

        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

        

    def post(self, request,pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.serializer_class(order , data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response( status=status.HTTP_400_BAD_REQUEST, data='Wrong parameters')        





class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()

        # Get the data from the request
        data = request.data

        # Extract the primary keys of the related Service instances
        service_pks = data.pop('services_list', None)

        # Extract the primary keys of the related Motor instances
        motor_pks = data.pop('motors_list', None)

        # Update the instance with the given data
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        order =  Order.objects.get(pk=kwargs["pk"])
        tech_name  =  order.technecian.user_id.full_name()
        
        if tech_name == request.user.full_name():
            serializer.save()
            # Update the many-to-many relationships of the Order instance
            if service_pks is not None:
                instance.services.set(service_pks)

            if motor_pks is not None:
                instance.motors.set(motor_pks)

            # Return a response with the updated instance data
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("error", status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)


        
    



class OrderAcceptView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, order_id):
        serializer = OrderAcceptSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['technecian_id']
            # user = self.request.user
            try:
                order = Order.objects.select_for_update().get(id=order_id, technecian=None, status='در آستانه کنسلی')
            except Order.DoesNotExist:
                return Response({'error': 'Order not found or already accepted by a technician'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                technecian = Technecian.objects.get(user_id=user)
            except Technecian.DoesNotExist:
                return Response({'error': 'Technecian not found'}, status=status.HTTP_400_BAD_REQUEST)
            order.technecian = technecian
            order.status = 'در حال انجام'
            order.save()
            return Response({'success': 'Order accepted successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderStats(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()
    
    def get(self, request):
        query_set = self.queryset
        user= request.user
        query_set = query_set.filter(technecian__user_id = user)
        sum_wage = query_set.aggregate(Sum('wage'))['wage__sum']
        sum_expanse = query_set.aggregate(Sum('expanse'))['expanse__sum']
        tech  = Technecian.objects.get(user_id= user)
        sum_trans = Transaction.objects.filter(technician=tech).aggregate(Sum('amount'))['amount__sum']
        total_commisions = query_set.aggregate(Order_com__sum=Sum('commission'))
        total_commisions = 0 if  total_commisions['Order_com__sum'] is None else total_commisions['Order_com__sum']
        total_credit = sum_trans - total_commisions
        total_recip = sum_expanse + sum_wage
        avg_grade = query_set.aggregate(Avg('grade'))['grade__avg']
        total_number_of_order = query_set.count()
        number_of_done_order = query_set.filter(status='انجام شد').count()
        data = {'total_number_of_order':total_number_of_order,'number_of_done_order':number_of_done_order
                ,'avg_grade':avg_grade,'total_credit':total_credit,'total_recip':total_recip}
        return Response(data=data, status=status.HTTP_200_OK)         


####### order-product ##############################
class OrderProductCreateView(generics.CreateAPIView):
    queryset = Order_Product.objects.all()
    serializer_class = OrderProductSerializer

    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(data=request.data)
        serializer.context['order'] = order
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderProductListView(generics.ListAPIView):
    serializer_class = OrderProductSerializer

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        return Order_Product.objects.filter(order__id=order_id)

class OrderProductUpdateView(generics.UpdateAPIView):
    queryset = Order_Product.objects.all()
    serializer_class = OrderProductSerializer

    def put(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            order = Order.objects.get(id=int(order_id))
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        order_product = Order_Product.objects.filter(order=order,product__id=data.product)
                    
        serializer = self.get_serializer(order_product, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Get the updated order products
        updated_order_products = Order_Product.objects.filter(order=order)
        serializer = self.get_serializer(updated_order_products, many=True)
        return Response(serializer.data)

class OrderProductBulkCreateView(generics.CreateAPIView):
    queryset = Order_Product.objects.all()
    serializer_class = OrderProductListSerializer

    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            order = Order.objects.get(id=int(order_id))
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        

        order_products = Order_Product.objects.filter(order=order)

        if len(order_products) == 0 :
            serializer = self.get_serializer(data=request.data)
            serializer.context['order'] = order
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        elif len(order_products) > 0:
            serializer = self.get_serializer(data=request.data)
            serializer.context['order'] = order
            serializer.is_valid(raise_exception=True)
            order_products.delete()
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)