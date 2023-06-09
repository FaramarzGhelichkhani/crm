import logging
import datetime
from django.contrib import messages
from django.shortcuts import  reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, Followup
from Transaction.models import Transaction
from EmdadUser.models import Technecian
from company.models import Expend
from datetime import date
from jalali_date import datetime2jalali
from django.db.models import Avg, Sum ,Q
from Transaction.forms import TransactionFormModel
from .forms import (
    OrderModelForm, 
    CustomUserCreationForm, 
    AssignAgentForm, 
    FollowUpModelForm
)


logger = logging.getLogger(__name__)


# # CRUD+L - Create, Retrieve, Update and Delete + List


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"
    
   
class DashboardView(LoginRequiredMixin,generic.TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        # user = self.request.user

        # leads stats
        total_lead_count = Order.objects.all().count()
        total_done = Order.objects.filter(status="انجام شد").count()
        total_cancel = Order.objects.filter(status= "کنسلی قطعی"  ).count()
        total_wage = Order.objects.filter(status="انجام شد").aggregate(total_wage=Sum('wage'))
        total_income = Transaction.objects.aggregate(total_income=Sum('amount'))
        # commssions
        total_commisions = 0 
        for row in Order.objects.exclude(technecian__isnull=True).values('technecian').annotate(sumcom=Sum('commission')):
            total_commisions += 0 if row['sumcom'] is None else row['sumcom']

        #expands
        total_expend = Expend.objects.all().aggregate(tot=Sum('amount'))


    #### today
        today = datetime.date.today() 
        total_in_today=Order.objects.filter(
            time__gte= today
        ).count()

        

        total_cancel_in_today=Order.objects.filter(
            time__gte= today  ,
            status= "کنسلی قطعی"
        ).count()    
        
        total_wage_today = Order.objects.filter(time__gte= today).aggregate(tot=Sum('wage'))
        total_commisions_today = 0 
        for row in Order.objects.filter(time__gte= today).exclude(technecian__isnull=True).values('technecian').annotate(sumwage=Sum('wage')):
            print(row)
            tech = Technecian.objects.get(pk=row['technecian'])
            total_commisions_today += row['sumwage'] * tech.commission
        
        # total_transaction_today  = Transaction.objects.filter(  time__gte= today ).aggregate(tot=Sum('amount'))
        
        
        
        context.update({
            "total_lead_count": total_lead_count,
            "total_in_today": total_in_today,
            "total_cancel_in_today":total_cancel_in_today,
            "total_cancel":total_cancel,
            "total_commisions_today": int(total_commisions_today),
            "total_wage_today": 0 if total_wage_today["tot"] is None else int(total_wage_today["tot"]),
            "total_transaction": int(total_wage['total_wage']),
            "total_commisions": int(total_commisions),
            "total_income":int(total_income["total_income"]),
            "total_done":total_done,
            "total_expend": int(total_expend["tot"]),
            "total_messeges": 0,
            "messeges_get_credit": 0 #messeges_get_credit

        })
        return context



def get_created_jalali(obj):
		return datetime2jalali(obj.time).strftime('%y/%m/%d %H:%M:%S')





# class TransactionsLeadListView(LoginRequiredMixin,generic.ListView):
#     template_name = "order/lead_list_transaction.html"
#     context_object_name = "leads"

#     def get_queryset(self):
#         if  self.kwargs.get("pk"):
#             agentid  = self.kwargs["pk"]
#             queryset = Order.objects.filter(status="انجام شد",transaction_status="تسویه نشده",
#             agent__id=agentid
#             ).extra(select={'com': 0}).order_by('-total_price_agent')
#         else:    
#             queryset = Order.objects.filter(status="انجام شد",transaction_status="تسویه نشده",
#             agent__isnull=False
#             ).extra(select={'com': 0}).order_by('-total_price_agent')
        
#         for lead in queryset:
#             lead.time = get_created_jalali(lead) 
#             com = (0 if Order.total_price_agent is None else Order.total_price_agent)* Order.agent.weight
#             Order.com = com
#         return queryset   



class TodayLeadListView(LoginRequiredMixin,generic.ListView):# LoginRequiredMixin
    template_name = "order/lead_list_today.html"
    context_object_name = "leads"

    def get_queryset(self):
        today = date.today() 
        if  self.kwargs.get("status"):
            status  = self.kwargs["status"]  
            queryset = Order.objects.filter(status__exact=status,time__year=today.year,
             time__month=today.month, time__day=today.day).order_by('-time')  
        else :    
            queryset = Order.objects.filter(
            time__year=today.year, time__month=today.month, time__day=today.day
            ).order_by('-time')
        return queryset

    def get_context_data(self, **kwargs):
        today = date.today()
        context = super(TodayLeadListView, self).get_context_data(**kwargs)
        agentqueryset = Order.objects.filter(
                technecian__isnull=True,
                 time__year=today.year, time__month=today.month,
                 time__day=today.day
            ).exclude(status = 'کنسلی قطعی')
        thresoldleads =  Order.objects.filter(status="در آستانه کنسلی" ,  
        time__year=today.year, time__month=today.month, time__day=today.day)    
        status =[]
        for s in Order.status_choices:
            status.append(s[0])
        context.update({
                "unassigned_leads": agentqueryset,
                "thresoldleads": thresoldleads,
                "status": status
            })
        return context


class LeadListView(LoginRequiredMixin,generic.ListView):# LoginRequiredMixin
    template_name = "order/lead_list.html"
    context_object_name = "leads"
    
    
    def get_queryset(self):
        agentquery  = Q(technecian_id=self.kwargs["pk"])   if  self.kwargs.get("pk")  else Q()
        status   = Q(status__exact= self.kwargs["status"]) if  self.kwargs.get("status")   else Q(status__isnull=False)
        phonequery=   Q(customer_phone__contains=self.request.GET.get("q") ) if  self.request.GET.get("q")  else Q()
        
        dataset = Order.objects.filter(
           agentquery &
            status
            & phonequery
            ).order_by('-time')[:200]
        
        for lead in dataset:
            lead.time = get_created_jalali(lead)
        return dataset
    


    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        if not self.kwargs.get("pk"):
            agentqueryset = Order.objects.filter(
                    technecian_id__isnull=True
                ).exclude(status = 'کنسلی قطعی')
            thresoldleads =  Order.objects.filter(status="در آستانه کنسلی" )    
            status = [  
            ]
            for s in Order.status_choices:
                status.append(s[0])
            context.update({
                    "unassigned_leads": agentqueryset,
                    "thresoldleads": thresoldleads,
                    "status": status
                })
        return context



class LeadDetailView(LoginRequiredMixin,generic.DetailView): 
    template_name = "order/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self,**kwargs):
        queryset = Order.objects.filter(id=self.kwargs["pk"])
        for lead in queryset:
            lead.time = get_created_jalali(lead)
        return queryset





class LeadCreateView(LoginRequiredMixin,generic.CreateView): #OrganisorAndLoginRequiredMixin
    template_name = "order/lead_create.html"
    form_class = OrderModelForm

    def get_success_url(self):
        return reverse("leads:lead-list-today")

    def form_valid(self, form):
        order = form.save(commit=False)
        order.save()
        
        # messeging
        # if order.customer_phone is not None and order.customer_messeg == True:
        #     full_name = Order.customer_full_name
        #     id = Order.id
        #     mobile = Order.customer_phone
        #     response =  send_messege_to_customer(id,mobile)
        #     m = Messages(lead=lead,groupId= response["Value"],status=response["StrRetStatus"],reciever=1)
        #     m.save()
        #     if  response["Value"]==11:
        #         Order.customer_messeg = False        
        # #send messeges to agent
        # if Order.agent is not None and Order.technician_messeg == True:
        #     response_send = send_messege_to_technician(
        #         customer_phone=Order.customer_phone,
        #         address=Order.address,
        #         problem=Order.problem,
        #         model= Order.motor_model,
        #         mobile=Order.agent.phone1)   
        #     m = Messages(lead=lead,groupId= response_send["Value"],status=response_send["StrRetStatus"],reciever=2)
        #     m.save()
        #     if response_send["Value"]==11 :
        #         Order.technician_messeg = False       
            
        # Order.save()
        messages.success(self.request, "You have successfully created a lead")
        return super(LeadCreateView, self).form_valid(form)




class LeadUpdateView(LoginRequiredMixin, generic.UpdateView): #OrganisorAndLoginRequiredMixin
    template_name = "order/lead_update.html"
    context_object_name = "lead"
    form_class = OrderModelForm

    def get_queryset(self,**kwargs):
        queryset = Order.objects.filter(id=self.kwargs["pk"])
        for lead in queryset:
            lead.time = get_created_jalali(lead)
        return queryset


    def get_success_url(self):
        return reverse("leads:lead-list-today")

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(LeadUpdateView, self).form_valid(form)



class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):#OrganisorAndLoginRequiredMixin
    template_name = "order/lead_delete.html"

    def get_success_url(self):
        return reverse("leads:lead-list-today")

    def get_queryset(self):
        return Order.objects.all()


class AssignAgentView(LoginRequiredMixin,generic.FormView):
    template_name = "order/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self):
        order =  Order.objects.get(pk=self.kwargs["pk"])   
        kwargs = super().get_form_kwargs()
        kwargs['initial']['agent'] = order.technecian
        kwargs['initial']['status'] = order.status
        return kwargs
    
    def get_success_url(self):
        return reverse("leads:lead-list-today")

    
    def form_valid(self, form):
        agent  = form.cleaned_data["agent"]
        status = form.cleaned_data["status"]
        order = Order.objects.get(id=self.kwargs["pk"])
    
        order.agent = agent
        order.status = status
        order.save()
        return super(AssignAgentView, self).form_valid(form)

class FollowUpCreateView(LoginRequiredMixin,generic.FormView):
    template_name = "order/followup_create.html"
    form_class = FollowUpModelForm

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowUpCreateView, self).get_context_data(**kwargs)
        context.update({
            "lead": Order.objects.get(pk=self.kwargs["pk"]),
            "user":self.request.user
        })
        return context


    def form_valid(self, form):
        lead = Order.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.order = lead
        
        grade_change = lead.grade != followup.grade
        lead.grade = followup.grade
        
        total_price_cusotmer_changed = lead.total_price_cusotmer != followup.total_price_cusotmer
        lead.total_price_cusotmer    = followup.total_price_cusotmer
        
        wage_changed = lead.wage != followup.total_wage_agent
        lead.wage = followup.total_wage_agent
        
        expanse_chnage = lead.expanse != followup.total_expanse_agent
        lead.expanse = followup.total_expanse_agent
        
        status_changed = lead.status != form.cleaned_data["status"]
        lead.status = form.cleaned_data["status"]
        lead.save()
        

      
        
        followup.notes += '\n'
        if grade_change:
            followup.notes +=  'امتیاز عملکرد تغییر یافت. '+ '\n'
        if total_price_cusotmer_changed:
            followup.notes += '.مقدار پرداختی مشتری تغییر یافت' + '\n'
        if wage_changed:
            followup.notes += 'اجرت تغییر یافت.' + '\n'
        if expanse_chnage:
            followup.notes += '.خرجکرد تغییر یافت' + '\n' 
        if status_changed:
            followup.notes += '.وضعیت سفارش تفییر یافت'         

        followup.save()
        
        return super(FollowUpCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        order =  Order.objects.get(pk=self.kwargs["pk"])   
        grade = order.grade
        total_expanse_agent = order.expanse
        total_wage_agent = order.wage
        kwargs = super().get_form_kwargs()
        kwargs['initial']['grade'] = grade
        kwargs['initial']['total_expanse_agent'] = total_expanse_agent
        kwargs['initial']['total_wage_agent'] = total_wage_agent
        kwargs['initial']['status'] = order.status
        kwargs['initial']['total_price_cusotmer'] = order.total_price_cusotmer
        return kwargs


class FollowUpUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = "order/followup_update.html"
    form_class  = FollowUpModelForm

    def get_queryset(self):
        queryset = Followup.objects.all()
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().order.id})

    def form_valid(self, form):
        followup = form.save(commit=False)
        order = followup.order 
        order.grade = followup.grade
        order.wage = followup.total_wage_agent
        order.expanse = followup.total_expanse_agent
        order.status = form.cleaned_data["status"]
        order.save()
        followup.save()
        

        return super(FollowUpUpdateView, self).form_valid(form)    


class FollowUpDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "order/followup_delete.html"

    def get_success_url(self):
        followup = Followup.objects.get(id=self.kwargs["pk"])
        return reverse("leads:lead-detail", kwargs={"pk": followup.Order.pk})

    def get_queryset(self):
        queryset = Followup.objects.all()
        return queryset





class TransactionListView(LoginRequiredMixin,generic.ListView): 
    template_name = "transactions/transactions_list.html"

    def get_queryset(self):
        if  self.kwargs.get("pk"):
            agentid  = self.kwargs["pk"]
            dataset = Transaction.objects.filter(
                technician__id=agentid
            ).order_by('-time')[:200]
            for tr in dataset:
                tr.time = get_created_jalali(tr)
            return dataset
        else:
            queryset  = Transaction.objects.all().order_by('-time')[:200]
            for tr in queryset:
                tr.time = get_created_jalali(tr)
            return queryset
                
    
   


class TransactionCreateView(LoginRequiredMixin,generic.CreateView): #OrganisorAndLoginRequiredMixin
    template_name = "transactions/transactions_create.html"
    form_class = TransactionFormModel

    def get_success_url(self):
        return reverse("transactions-list")

    def form_valid(self, form):
        transaction = form.save(commit=False)
        messages.success(self.request, "ایجاد شد")   
        transaction.save()
        return super(TransactionCreateView, self).form_valid(form)    

    def get_form_kwargs(self):
        agent =  Technecian.objects.get(pk=self.kwargs["pk"])   
        
        kwargs = super().get_form_kwargs()
        kwargs['initial']['technician'] = agent
        
        return kwargs
        
  

class TransactionUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = "transactions/transactions_update.html"
    form_class = TransactionFormModel

    def get_success_url(self):
        return reverse("transactions-list")

    def get_queryset(self):
        return Transaction.objects.all()
    



class TransactionDeleteView(LoginRequiredMixin,generic.DeleteView): 
    template_name = "transactions/transactions_delete.html"
    context_object_name = "Transaction"

    def get_success_url(self):
        return reverse("transactions-list")

    def get_queryset(self):
        return Transaction.objects.all()


# class MessegesListView(LoginRequiredMixin,generic.ListView): 
#     template_name = "Messeges/messeges_list.html"

#     def get_queryset(self):
#         queryset = Messages.objects.all().order_by('-id')
#         for ms in queryset:
#             ms.time = get_created_jalali(ms)
#         return queryset