
import logging
import datetime
from django import contrib
from django.contrib import messages
from django.core.mail import send_mail
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from django_genericfilters.views import FilteredListView
# from agents.mixins import OrganisorAndLoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lead, Agent, FollowUp, Transaction, Messages
from company.models import Expend
from datetime import date
from jalali_date import datetime2jalali,date2jalali
from django.db.models import Avg, Sum ,Q
from .sms.script import send_messege_to_customer, send_messege_to_technician, get_credit

from .forms import (
    # LeadForm, 
    LeadModelForm, 
    TransactionFormModel,
    CustomUserCreationForm, 
    AssignAgentForm, 
    # # LeadCategoryUpdateForm,
    # # CategoryModelForm,
    # FollowUpForm,
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
    
    # def get_success_url(self):
    #     return reverse("leads:lead-list-today")

# #     def dispatch(self, request, *args, **kwargs):
# #         if request.user.is_authenticated:
# #             return redirect("dashboard")
# #         return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin,generic.TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        # user = self.request.user

        # How many leads we have in total
        total_lead_count = Lead.objects.all().count()

        today = datetime.date.today() 
        total_in_today=Lead.objects.filter(
            time__gte= today
        ).count()

        total_cancel = Lead.objects.filter(
              status= "کنسلی قطعی"  ).count()

        total_cancel_in_today=Lead.objects.filter(
            time__gte= today  ,
            status= "کنسلی قطعی"
        ).count()


        total_done = Lead.objects.filter(status="انجام شد").count()

        total_transaction  = Transaction.objects.filter(category="دریافتی از سفارش").aggregate(total_transactions=Sum('total_amount'))
        total_commisions = Transaction.objects.filter(category="دریافتی از سفارش").aggregate(total_commisions=Sum('company_amount'))
        total_income = Transaction.objects.filter(category="واریزی توسط تکنسین").aggregate(total_income=Sum('total_amount'))

        total_transaction_today  = Transaction.objects.filter(  time__gte= today , category="دریافتی از سفارش").aggregate(tot=Sum('total_amount'))
        total_commisions_today = Transaction.objects.filter(time__gte= today  , category="دریافتی از سفارش").aggregate(tot=Sum('company_amount'))

        total_expend = Expend.objects.all().aggregate(tot=Sum('amount'))
        total_messeges = Messages.objects.all().count()
        # messeges_get_credit = get_credit()
        
        context.update({
            "total_lead_count": total_lead_count,
            "total_in_today": total_in_today,
            "total_cancel_in_today":total_cancel_in_today,
            "total_cancel":total_cancel,
            "total_transaction_today":0 if total_transaction_today["tot"] is None else int(total_transaction_today["tot"]),
            "total_commisions_today": 0 if total_commisions_today["tot"] is None else int(total_commisions_today["tot"]),
            "total_transaction": int(total_transaction["total_transactions"]),
            "total_commisions": int(total_commisions["total_commisions"]),
            "total_income":int(total_income["total_income"]),
            "total_done":total_done,
            "total_expend": int(total_expend["tot"]),
            "total_messeges": total_messeges,
            "messeges_get_credit": 0 #messeges_get_credit

        })
        return context


# # def landing_page(request):
# #     return render(request, "landing.html")

def get_created_jalali(obj):
		return datetime2jalali(obj.time).strftime('%y/%m/%d %H:%M:%S')







class TransactionsLeadListView(LoginRequiredMixin,generic.ListView):# LoginRequiredMixin
    template_name = "leads/lead_list_transaction.html"
    context_object_name = "leads"

    def get_queryset(self):
        if  self.kwargs.get("pk"):
            agentid  = self.kwargs["pk"]
            queryset = Lead.objects.filter(status="انجام شد",transaction_status="تسویه نشده",
            agent__id=agentid
            ).extra(select={'com': 0}).order_by('-total_price_agent')
        else:    
            queryset = Lead.objects.filter(status="انجام شد",transaction_status="تسویه نشده",
            agent__isnull=False
            ).extra(select={'com': 0}).order_by('-total_price_agent')
        
        for lead in queryset:
            lead.time = get_created_jalali(lead) 
            com = (0 if lead.total_price_agent is None else lead.total_price_agent)* lead.agent.weight
            lead.com = com
        return queryset   

    # def get_context_data(self, **kwargs):
    #     context = super(TransactionsLeadListView, self).get_context_data(**kwargs) 
    #     queryset = context["leads"]
    #     commision =[]
    #     for lead in queryset:
    #         com = (0 if lead.total_price_agent is None else lead.total_price_agent)* lead.agent.weight
    #         commision.append(com)
    #     context.update({
    #             "data": commision
    #         })
    #     return context


class TodayLeadListView(LoginRequiredMixin,generic.ListView):# LoginRequiredMixin
    template_name = "leads/lead_list_today.html"
    context_object_name = "leads"

    def get_queryset(self):
        today = date.today() 
        if  self.kwargs.get("status"):
            status  = self.kwargs["status"]  
            queryset = Lead.objects.filter(status__exact=status,time__year=today.year,
             time__month=today.month, time__day=today.day).order_by('-time')  
        else :    
            queryset = Lead.objects.filter(
            time__year=today.year, time__month=today.month, time__day=today.day
            ).order_by('-time')
        return queryset

    def get_context_data(self, **kwargs):
        today = date.today()
        context = super(TodayLeadListView, self).get_context_data(**kwargs)
        agentqueryset = Lead.objects.filter(
                agent__isnull=True,
                 time__year=today.year, time__month=today.month,
                 time__day=today.day
            ).exclude(status = 'کنسلی قطعی')
        thresoldleads =  Lead.objects.filter(status="در آستانه کنسلی" ,  
        time__year=today.year, time__month=today.month, time__day=today.day)    
        status =[]
        for s in Lead.status_choices:
            status.append(s[0])
        context.update({
                "unassigned_leads": agentqueryset,
                "thresoldleads": thresoldleads,
                "status": status
            })
        return context


class LeadListView(LoginRequiredMixin,generic.ListView):# LoginRequiredMixin
    template_name = "leads/lead_list.html"
    context_object_name = "leads"
    
    
    def get_queryset(self):
        agentquery  = Q(agent__id=self.kwargs["pk"])  if  self.kwargs.get("pk")  else Q()
        status   = self.kwargs["status"]    if  self.kwargs.get("status")   else Q(status__isnull=False)
        phonequery=   Q(customer_phone__contains=self.request.GET.get("q") ) if  self.request.GET.get("q")  else Q()
        dataset = Lead.objects.filter(
           agentquery &
            Q(status__exact= status) 
            & phonequery
            ).order_by('-time')[:200]
        for lead in dataset:
            lead.time = get_created_jalali(lead)
        return dataset
    


    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        if not self.kwargs.get("pk"):
            agentqueryset = Lead.objects.filter(
                    agent__isnull=True
                ).exclude(status = 'کنسلی قطعی')
            thresoldleads =  Lead.objects.filter(status="در آستانه کنسلی" )    
            status = [  
            ]
            for s in Lead.status_choices:
                status.append(s[0])
            context.update({
                    "unassigned_leads": agentqueryset,
                    "thresoldleads": thresoldleads,
                    "status": status
                })
        return context


# def lead_list(request):
#     leads = Lead.objects.all()
#     context = {
#         "leads": leads
#     }
#     return render(request, "leads/lead_list.html", context)


class LeadDetailView(LoginRequiredMixin,generic.DetailView): #LoginRequiredMixin
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"
    # queryset = Lead.objects.get(id=self.kwargs["pk"])
    def get_queryset(self,**kwargs):
        queryset = Lead.objects.filter(id=self.kwargs["pk"])
        for lead in queryset:
            lead.time = get_created_jalali(lead)
        return queryset


# def lead_detail(request, pk):
#     lead = Lead.objects.get(id=pk)
#     context = {
#         "lead": lead
#     }
#     return render(request, "leads/lead_detail.html", context)


class LeadCreateView(LoginRequiredMixin,generic.CreateView): #OrganisorAndLoginRequiredMixin
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list-today")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.save()
            # send messege to customer
        if lead.customer_phone is not None and lead.customer_messeg == True:
            full_name = lead.customer_full_name
            id = lead.id
            mobile = lead.customer_phone
            response =  send_messege_to_customer(id,mobile)
            m = Messages(lead=lead,groupId= response["Value"],status=response["StrRetStatus"],reciever=1)
            m.save()
            if  response["Value"]==11:
                lead.customer_messeg = False        
        #send messeges to agent
        if lead.agent is not None and lead.technician_messeg == True:
            response_send = send_messege_to_technician(
                customer_phone=lead.customer_phone,
                address=lead.address,
                problem=lead.problem,
                model= lead.motor_model,
                mobile=lead.agent.phone1)   
            m = Messages(lead=lead,groupId= response_send["Value"],status=response_send["StrRetStatus"],reciever=2)
            m.save()
            if response_send["Value"]==11 :
                lead.technician_messeg = False       
            
        lead.save()
        messages.success(self.request, "You have successfully created a lead")
        return super(LeadCreateView, self).form_valid(form)



# def lead_create(request):
#     form = LeadModelForm()
#     if request.method == "POST":
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("/leads")
#     context = {
#         "form": form
#     }
#     return render(request, "leads/lead_create.html", context)


class LeadUpdateView(LoginRequiredMixin, generic.UpdateView): #OrganisorAndLoginRequiredMixin
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self,**kwargs):
        queryset = Lead.objects.filter(id=self.kwargs["pk"])
        for lead in queryset:
            lead.time = get_created_jalali(lead)
        return queryset


    def get_success_url(self):
        return reverse("leads:lead-list-today")

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(LeadUpdateView, self).form_valid(form)


# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadModelForm(instance=lead)
#     if request.method == "POST":
#         form = LeadModelForm(request.POST, instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect("/leads")
#     context = {
#         "form": form,
#         "lead": lead
#     }
#     return render(request, "leads/lead_update.html", context)


class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):#OrganisorAndLoginRequiredMixin
    template_name = "leads/lead_delete.html"

    def get_success_url(self):
        return reverse("leads:lead-list-today")

    def get_queryset(self):
        # user = self.request.user
        # initial queryset of leads for the entire organisation
        return Lead.objects.all()


# def lead_delete(request, pk):
#     lead = Lead.objects.get(id=pk)
#     lead.delete()
#     return redirect("/leads")


class AssignAgentView(LoginRequiredMixin,generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self):
        lead =  Lead.objects.get(pk=self.kwargs["pk"])   
        kwargs = super().get_form_kwargs()
        kwargs['initial']['agent'] = lead.agent
        kwargs['initial']['status'] = lead.status
        return kwargs
    
    def get_success_url(self):
        return reverse("leads:lead-list-today")

    
    def form_valid(self, form):
        agent  = form.cleaned_data["agent"]
        status = form.cleaned_data["status"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        if lead.agent != agent:
            # send_messeges to agent
            response_send = send_messege_to_technician(
            customer_phone=lead.customer_phone,
            address=lead.address,
            problem=lead.problem,
            model= lead.motor_model,
            mobile=agent.phone1)   
            m = Messages(lead=lead,groupId= response_send["Value"],status=response_send["StrRetStatus"],reciever=2)
            m.save()
            if response_send["Value"]==11:
                lead.technician_messeg = False
        lead.agent = agent
        lead.status = status
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class FollowUpCreateView(LoginRequiredMixin,generic.FormView):
    template_name = "leads/followup_create.html"
    form_class = FollowUpModelForm

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowUpCreateView, self).get_context_data(**kwargs)
        context.update({
            "lead": Lead.objects.get(pk=self.kwargs["pk"]),
        })
        return context


    def form_valid(self, form):
        lead = Lead.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.lead = lead
        followup.save()
        lead.grade = followup.grade
        lead.total_price_agent = followup.total_price_agent
        lead.total_price_cusotmer = followup.total_price_cusotmer
        lead.status = form.cleaned_data["status"]
        lead.transaction_status = form.cleaned_data["tr_status"]
        lead.save()
        if lead.status == "انجام شد"  and not form.cleaned_data["total_price_agent"]  is None :
            if not Transaction.objects.filter(order=lead).exists():
                company_amount = lead.total_price_agent* lead.agent.weight
                m = Transaction(technician = lead.agent,  order=lead , total_amount = lead.total_price_agent , company_amount =company_amount , category = "دریافتی از سفارش")
                m.save()
            else:
                tr =   Transaction.objects.get(order=lead)
                tr.total_amount = lead.total_price_agent
                company_amount = lead.total_price_agent* lead.agent.weight
                tr.company_amount= company_amount
                tr.save()
        return super(FollowUpCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        lead =  Lead.objects.get(pk=self.kwargs["pk"])   
        grade = lead.grade
        total_price_cusotmer = lead.total_price_cusotmer
        total_price_agent = lead.total_price_agent
        kwargs = super().get_form_kwargs()
        kwargs['initial']['grade'] = grade
        kwargs['initial']['total_price_cusotmer'] = total_price_cusotmer
        kwargs['initial']['total_price_agent'] = total_price_agent
        kwargs['initial']['status'] = lead.status
        kwargs['initial']['tr_status'] = lead.transaction_status
        return kwargs


class FollowUpUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = "leads/followup_update.html"
    form_class  = FollowUpModelForm

    def get_queryset(self):
        # agent = self.request.agent
        # id  = self.kwargs["pk"]
        # queryset = self.request.filter(lead__id=id)
        queryset = FollowUp.objects.all()
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().lead.id})

    def form_valid(self, form):
        followup = form.save(commit=False)
        lead = followup.lead 
        lead.grade = followup.grade
        lead.total_price_agent = followup.total_price_agent
        lead.total_price_cusotmer = followup.total_price_cusotmer
        lead.status = form.cleaned_data["status"]
        lead.transaction_status = form.cleaned_data["tr_status"]
        lead.save()
        followup.save()
        if lead.status == "انجام شد"  and not form.cleaned_data["total_price_agent"]  is None :
            if not Transaction.objects.filter(order=lead).exists():
                company_amount = lead.total_price_agent* lead.agent.weight
                m = Transaction(technician = lead.agent,  order=lead , total_amount = lead.total_price_agent , company_amount =company_amount , category = "دریافتی از سفارش")
                m.save()
            else:
                tr =   Transaction.objects.get(order=lead)
                tr.total_amount = lead.total_price_agent
                company_amount = lead.total_price_agent* lead.agent.weight
                tr.company_amount= company_amount
                tr.save()

        return super(FollowUpUpdateView, self).form_valid(form)    


class FollowUpDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "leads/followup_delete.html"

    def get_success_url(self):
        followup = FollowUp.objects.get(id=self.kwargs["pk"])
        return reverse("leads:lead-detail", kwargs={"pk": followup.lead.pk})

    def get_queryset(self):
        # lead = Lead.objects.get(id=self.kwargs["pk"])
        queryset = FollowUp.objects.all()
        # queryset = queryset.filter(lead=lead)
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
                
    

   

    # def get_queryset(self):
    #     filter_val = self.request.GET.get('filter', 'give-default-value')
    #     # order = self.request.GET.get('orderby', 'give-default-value')
    #     new_context = Transaction.objects.filter(
    #         technician=filter_val
    #     ).order_by(time)
    #     return new_context

    # def get_context_data(self, **kwargs):
    #     context = super(MyView, self).get_context_data(**kwargs)
    #     context['filter'] = self.request.GET.get('filter', 'give-default-value')
    #     # context['orderby'] = self.request.GET.get('orderby', 'give-default-value')
    #     return context


   


class TransactionCreateView(LoginRequiredMixin,generic.CreateView): #OrganisorAndLoginRequiredMixin
    template_name = "transactions/transactions_create.html"
    form_class = TransactionFormModel

    def get_success_url(self):
        return reverse("transactions-list")

    def form_valid(self, form):
        transaction = form.save(commit=False)
        if transaction.category== "واریزی توسط تکنسین" and transaction.total_amount != transaction.company_amount:
            messages.error(self.request, "مقدار سهم شرکت و دریافتی کل باید بکسان باشد")
            return self.form_invalid(form)
        elif  transaction.category== "واریزی توسط تکنسین" and transaction.total_amount == transaction.company_amount:
            messages.success(self.request, "ایجاد شد")   
            transaction.save()
            for orderid in self.request.POST.getlist('orders'):
                l = Lead.objects.get(id=int(orderid))
                l.transaction_status = "تسویه شد"
                l.save()
        else:  
            transaction.save()
        return super(TransactionCreateView, self).form_valid(form)    

    def get_form_kwargs(self):
        agent =  Agent.objects.get(pk=self.kwargs["pk"])   
        orders = Lead.objects.filter(
            transaction_status="تسویه نشده",agent=agent, status = 'انجام شد')
        kwargs = super().get_form_kwargs()
        kwargs['initial']['technician'] = agent
        kwargs['initial']['order'] = orders 
        kwargs['initial']['category'] = "واریزی توسط تکنسین" 
        kwargs['initial']['cat'] = "واریزی توسط تکنسین" 
        kwargs['initial']['tech'] = agent.first_name + ' '+ agent.last_name
        kwargs['initial']['cat'] = "واریزی توسط تکنسین" 
        return kwargs
        
  

class TransactionUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = "transactions/transactions_update.html"
    form_class = TransactionFormModel
    # context_object_name = "Transaction"

    def get_success_url(self):
        return reverse("transactions-list")

    def get_queryset(self):
        return Transaction.objects.all()
    
    # def get_form_kwargs(self,form):
    #     # tr = Transaction.objects.get(pk=self.kwargs["pk"])   
    #     # tr.technician
    #     tr = form.save(commit=False)
    #     print("$$$$$$$$$$$$$$$$$$$$4",tr.order)
    #     kwargs = super().get_form_kwargs()
    #     kwargs['initial']['technician'] = tr.technician
    #     kwargs['initial']['tech'] = tr.technician.first_name + ' '+ tr.technician.last_name
    #     kwargs['initial']['cat'] = "واریزی توسط تکنسین" 
    #     kwargs['initial']['order'] = tr.order.queryset 
    #     # kwargs['initial']['category'] = "واریزی توسط تکنسین" 
    #     return kwargs    
     


class TransactionDeleteView(LoginRequiredMixin,generic.DeleteView): 
    template_name = "transactions/transactions_delete.html"
    context_object_name = "Transaction"

    def get_success_url(self):
        return reverse("transactions-list")

    def get_queryset(self):
        return Transaction.objects.all()


class MessegesListView(LoginRequiredMixin,generic.ListView): 
    template_name = "Messeges/messeges_list.html"

    def get_queryset(self):
        queryset = Messages.objects.all().order_by('-id')
        for ms in queryset:
            ms.time = get_created_jalali(ms)
        return queryset
                
    

# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             lead.customer_full_name = customer_full_name
#             lead.first_name = customer_phone
#             lead.problem = problem
#             lead.save()
#             return redirect("/leads")
#     context = {
#         "form": form,
#         "lead": lead
#     }
#     return render(request, "leads/lead_update.html", context)


# def lead_create(request):
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             agent = Agent.objects.first()
#             Lead.objects.create(
#                 customer_full_name=customer_full_name,
#                 customer_phone=customer_phone,
#                 agent=agent
#             )
#             return redirect("/leads")
#     context = {
#         "form": form
#     }
#     return render(request, "leads/lead_create.html", context)


# class LeadJsonView(generic.View):

#     def get(self, request, *args, **kwargs):
        
#         qs = list(Lead.objects.all().values(
#             "customer_full_name", 
#             "customer_phone", 
#             "problem")
#         )

#         return JsonResponse({
#             "qs": qs,
#         })