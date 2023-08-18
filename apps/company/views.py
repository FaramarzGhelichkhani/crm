from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import *
from .models import *
from apps.Order.crm_views import get_created_jalali

class ExpendListView(LoginRequiredMixin,generic.ListView):# 
    template_name = "Expends/expend_list.html"
    # context_object_name = "expands"

    def get_queryset(self):
        queryset  = Expend.objects.all().order_by('-time')
        for exp in queryset:
            exp.time = get_created_jalali(exp)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ExpendListView, self).get_context_data(**kwargs)
        return context

class ExpendCreateView(LoginRequiredMixin,generic.CreateView): #
    template_name = "Expends/expend_create.html"
    form_class = ExpendModelForm

    def get_success_url(self):
        return reverse("company:expend-list")

class ExpendUpdateView(LoginRequiredMixin, generic.UpdateView): #OrganisorAndLoginRequiredMixin
    template_name = "Expends/expend_update.html"
    form_class = ExpendModelForm
    context_object_name = "expands"


    def get_queryset(self,**kwargs):
        queryset = Expend.objects.filter(id=self.kwargs["pk"])
        return queryset


    def get_success_url(self):
        return reverse("company:expend-list")

    # def form_valid(self, form):
    #     form.save()
    #     messages.info(self.request, "You have successfully updated this lead")
    #     return super(ExpendUpdateView, self).form_valid(form)
