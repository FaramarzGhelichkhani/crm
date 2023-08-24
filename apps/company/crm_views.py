from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from apps.Order.models import Order
from apps.Transaction.models import Transaction
from .models import Technician
from .forms import AgentModelForm, UserModelForm, reciptForm
from django.db.models import Avg, Sum, Q
from datetime import datetime, timedelta, time
from jalali_date import datetime2jalali


class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    queryset = Technician.objects.all()


class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")


class UserCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "agents/user_create.html"
    form_class = UserModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")


class AgentDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        return Technician.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AgentDetailView, self).get_context_data(**kwargs)
        agent = Technician.objects.get(id=self.kwargs["pk"])
        leads = Order.objects.filter(technician__id=self.kwargs["pk"])

        total_lead_number = leads.count()
        total_sucess_lead_number = Order.objects.filter(
            technician__id=self.kwargs["pk"], status=Order.DONE).count()
        grade_avg = Order.objects.filter(
            technician__id=self.kwargs["pk"], status=Order.DONE).aggregate(Avg('grade'))

        total_transaction_deposit = Transaction.objects.filter(technician__id=self.kwargs["pk"])\
            .aggregate(Transaction_amount__sum=Sum('amount'))

        total_deposit = 0 if total_transaction_deposit[
            'Transaction_amount__sum'] is None else total_transaction_deposit['Transaction_amount__sum']

        total_wage = leads.aggregate(Order_wage__sum=Sum('wage'))[
            "Order_wage__sum"]
        total_commisions = leads.filter(status=Order.DONE).aggregate(
            Order_com__sum=Sum('commission'))
        total_commisions = 0 if total_commisions['Order_com__sum'] is None else total_commisions['Order_com__sum']

        bedehi = total_commisions - total_deposit

        agent.balance = bedehi

        agent.save()
        context.update({
            "total_lead_number": total_lead_number,
            "total_sucess_lead_number": total_sucess_lead_number,
            "grade_avg": 0 if grade_avg['grade__avg'] is None else round(float(grade_avg['grade__avg']), 1),
            "total_wage": total_wage,
            "total_commisions": total_commisions,
            "total_deposite": total_deposit,
            "bedehi": bedehi
        })
        return context


class AgentUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    context_object_name = "agent"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        return Technician.objects.all()


class AgentDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        return Technician.objects.all()


class MakeRecepieListView(LoginRequiredMixin, generic.FormView):
    template_name = "agents/agent_make_recipe.html"
    form_class = reciptForm

    def get_success_url(self):
        gt = self.request.POST.get('start_date_offset')
        lt = self.request.POST.get('end_date_offset')
        return reverse("agents:agent-lead-list-transactions",
                       kwargs={'pk': self.kwargs["pk"], 'gt': gt, 'lt': lt})


def get_created_jalali_recip(obj):
    return datetime2jalali(obj.time).strftime('14%y/%m/%d')


class RecepieListView(LoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_lead_recipe.html"
    context_object_name = "leads"

    def update_balance(self, agent_id, max_date=None):

        if max_date is None:
            leads = Order.objects.filter(
                technician__id=agent_id, status=Order.DONE)
            transactions = Transaction.objects.filter(technician__id=agent_id)
        else:
            transactions = Transaction.objects.filter(
                technician__id=agent_id, time__lt=max_date)
            leads = Order.objects.filter(
                technician__id=agent_id, time__lt=max_date, status=Order.DONE)

        agent = Technician.objects.get(id=agent_id)

        total_transaction_deposit = transactions.aggregate(
            Transaction_amount__sum=Sum('amount'))

        total_deposit = 0 if total_transaction_deposit[
            'Transaction_amount__sum'] is None else total_transaction_deposit['Transaction_amount__sum']

        total_commisions = leads.aggregate(Order_com__sum=Sum('commission'))
        total_commisions = 0 if total_commisions['Order_com__sum'] is None else total_commisions['Order_com__sum']

        bedehi = total_commisions - total_deposit

        if max_date is None:
            agent.balance = bedehi
            agent.save()

        return bedehi

    def get_date_offset(self, offset):
        today = datetime.now()
        date = today - timedelta(days=int(offset))
        return datetime.combine(date.date(), time.min)

    def get_queryset(self):
        agentid = self.kwargs["pk"]
        gt_time = self.get_date_offset(self.kwargs["gt"])
        lt_time = datetime.combine(
            self.get_date_offset(self.kwargs["lt"]), time.max)
        order_queryset = Order.objects.filter(
            Q(status=Order.DONE) &
            Q(technician__id=agentid) &
            Q(time__gte=gt_time)
            &
            Q(time__lte=lt_time)
        )\
            .order_by('time')

        for lead in order_queryset:
            lead.time = get_created_jalali_recip(lead)

        return order_queryset

    def get_context_data(self, **kwargs):
        order_queryset = self.get_queryset()
        context = super(RecepieListView, self).get_context_data(**kwargs)
        agentqueryset = Technician.objects.get(id=self.kwargs["pk"])
        gt_time = self.get_date_offset(self.kwargs["gt"])
        lt_time = datetime.combine(
            self.get_date_offset(self.kwargs["lt"]), time.max)

        transaction_quetyset = Transaction.objects.filter(
            Q(technician=agentqueryset.id) &
            Q(time__gte=gt_time)
            &
            Q(time__lte=lt_time)
        )

        for trans in transaction_quetyset:
            trans.time = get_created_jalali_recip(trans)

        total_wages = order_queryset.aggregate(tot_com=Sum('wage'))
        total_commisions = order_queryset.aggregate(
            Order_com__sum=Sum('commission'))

        total_transaction = transaction_quetyset.aggregate(Sum('amount'))

        total_tr = 0 if total_transaction['amount__sum'] is None else total_transaction['amount__sum']
        total_wage = 0 if total_wages["tot_com"] is None else int(
            total_wages["tot_com"])
        total_commisions = 0 if total_commisions['Order_com__sum'] is None else total_commisions['Order_com__sum']

        bedehi = total_commisions - total_tr
        total_bedehi = self.update_balance(agentqueryset.id, max_date=None)
        initial_bedehi = self.update_balance(
            agentqueryset.id, max_date=self.get_date_offset(self.kwargs["gt"]))

        context.update({
            "from": self.get_date_offset(self.kwargs["gt"]),
            "to": self.get_date_offset(self.kwargs["lt"]),
            "agent": agentqueryset,
            "transactions": transaction_quetyset,
            "total_wage": total_wage,
            "total_tr": total_tr,
            "total_commisions": total_commisions,
            "bedehi": bedehi,
            "initial_bedehi": initial_bedehi,
            "total_bedehi": total_bedehi
        })
        return context
