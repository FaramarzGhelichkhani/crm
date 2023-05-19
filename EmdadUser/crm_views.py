import random

from django.core.mail import send_mail
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from Order.models import Order
from Transaction.models import Transaction
from .models import Technecian
from .forms import AgentModelForm, UserModelForm
from django.db.models import Avg, Sum
from Order.crm_views import get_created_jalali
from jalali_date import datetime2jalali,date2jalali


class AgentListView(LoginRequiredMixin, generic.ListView): #OrganisorAndLoginRequiredMixin
    template_name = "agents/agent_list.html"
    queryset  = Technecian.objects.all()
   


class AgentCreateView(LoginRequiredMixin,generic.CreateView): #OrganisorAndLoginRequiredMixin
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")


class UserCreateView(LoginRequiredMixin,generic.CreateView): #OrganisorAndLoginRequiredMixin
    template_name = "agents/user_create.html"
    form_class = UserModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")



class AgentDetailView(LoginRequiredMixin,generic.DetailView): #OrganisorAndLoginRequiredMixin
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        return Technecian.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AgentDetailView, self).get_context_data(**kwargs)
        agent = Technecian.objects.get(id = self.kwargs["pk"] )
        leads = Order.objects.filter(technecian__id=self.kwargs["pk"])
        total_lead_number =  leads.count()
        total_sucess_lead_number =  Order.objects.filter(technecian__id=self.kwargs["pk"],status="انجام شد").count()
        grade_avg = Order.objects.filter(technecian__id=self.kwargs["pk"],status="انجام شد").aggregate(Avg('grade'))
        
        total_transaction_deposit = Transaction.objects.filter(technician__id=self.kwargs["pk"])\
        .aggregate(Transaction_amount__sum=Sum('amount'))
        
        total_deposit = 0 if  total_transaction_deposit['Transaction_amount__sum'] is None else total_transaction_deposit['Transaction_amount__sum'] 
        
        total_wage = leads.aggregate(Order_wage__sum=Sum('wage'))
        total_wage = 0 if  total_wage['Order_wage__sum'] is None else total_wage['Order_wage__sum']
        total_commisions = int(total_wage * agent.commission)

   
        bedehi = total_commisions - total_deposit 
        
        agent.balance = bedehi
        
        agent.save()
        context.update({
                "total_lead_number": total_lead_number , 
                "total_sucess_lead_number": total_sucess_lead_number,
                "grade_avg":0  if  grade_avg['grade__avg'] is  None else round(float(grade_avg['grade__avg']),1) ,
                "total_wage": total_wage,
                "total_commisions": total_commisions,
                "total_deposite":total_deposit ,
                "bedehi": bedehi
            })
        return context

class AgentUpdateView(LoginRequiredMixin,generic.UpdateView):#OrganisorAndLoginRequiredMixin
    template_name = "agents/agent_update.html"
    context_object_name = "agent"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        return Technecian.objects.all()
    #     organisation = self.request.user.userprofile
    #     return Agent.objects.filter(organisation=organisation)


class AgentDeleteView(LoginRequiredMixin,generic.DeleteView): #OrganisorAndLoginRequiredMixin
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        # organisation = self.request.user.userprofile
        return Technecian.objects.all()

class RecepieListView(LoginRequiredMixin,generic.ListView):# LoginRequiredMixin
    template_name = "agents/agent_lead_recipe.html"
    context_object_name = "leads"

    def get_queryset(self):
        agentid  = self.kwargs["pk"]
        queryset = Order.objects.filter(status="انجام شد",
        agent__id=agentid
        ).extra(select={'com': 0}).order_by('-time')
        for lead in queryset:
            lead.time = get_created_jalali(lead) 
            com = (0 if lead.total_price_agent is None else lead.total_price_agent)* lead.technecian.commission
            lead.com = int(com)
        return queryset  

    def get_context_data(self, **kwargs):
        context = super(RecepieListView, self).get_context_data(**kwargs)
        agentqueryset = Technecian.objects.get(id=self.kwargs["pk"])
        
        leads = Order.objects.filter(technecian__id=self.kwargs["pk"])
        total_commisions = leads.aggregate(tot_com=Sum('wage'))

        
        total_transaction = Transaction.objects.filter(technician__id=self.kwargs["pk"])\
        .aggregate(Sum('amount'))

        total_tr = 0 if  total_transaction['amount__sum'] is None else total_transaction['amount__sum'] 
        total_com = 0 if total_commisions["tot_com"] is None else int(total_commisions["tot_com"])
        context.update({
                "agent": agentqueryset,
                "total_tr": total_tr,
                "total_commisions":total_com
            })
        return context 


# def CreateRecepie(request,pk):
#     from reportlab.platypus import SimpleDocTemplate
#     from reportlab.platypus.tables import Table
#     from reportlab.platypus import Paragraph
#     from reportlab.platypus import TableStyle
#     from reportlab.lib import colors
#     import io
#     from django.http import FileResponse
#     from reportlab.pdfgen import canvas
#     from reportlab.lib.pagesizes import letter, A4
#     from reportlab.lib.enums import TA_RIGHT
#     from reportlab.pdfbase import pdfmetrics
#     from reportlab.pdfbase.ttfonts import TTFont
#     import arabic_reshaper
#     from reportlab.platypus import Frame, PageTemplate , Spacer
#     from bidi.algorithm import get_display
#     from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
#     from reportlab.lib.units import mm,inch ,cm
#     import datetime
#     from reportlab.platypus.flowables import TopPadder


#     # Create a file-like buffer to receive PDF data.
#     buffer = io.BytesIO()

#     # Create the PDF object, using the buffer as its "file."
#     c = canvas.Canvas(buffer,pagesize=A4)

#     # Draw things on the PDF. Here's where the PDF generation happens.
#     # See the ReportLab documentation for the full list of functionality. 
#     c.setTitle('Recepie')
#     c.setAuthor('Emdad Motor')
#     c.setSubject('tasfie')





#     pdfmetrics.registerFont(TTFont('Persian', 'Shabnam.ttf'))
#     # styles = getSampleStyleSheet()
#     # styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT, fontName='Persian', fontSize=10))
#     doc = SimpleDocTemplate("test.pdf",pagesize=A4)# rightMargin=0, leftMargin=6.5 * cm, topMargin=0.3 * cm, bottomMargin=0)
    
#     style = TableStyle([
#     ('BACKGROUND',(0,0),(6,0),colors.green),
#     ('TEXTCOLOR',(0,0),(6,0),colors.whitesmoke),
#     ('BACKGROUND',(0,1),(6,-2),colors.beige),
#     ('BACKGROUND',(0,-1),(6,-1),colors.burlywood),
#     ('INNERGRID', (0,0), (-1,-1), 0.25, colors.white),
#     ('ALIGNMENT' , (0,0),(6,0), TA_RIGHT),
#     ('ALIGN' , (0,0) , (-1,-1),   'CENTER' ),
#     ('VALIGN',(0,0),(-1,-1),'BOTTOM'),
#     ('FONTNAME', (0,0), (-1,-1), 'Persian'),
#     ('FONTSIZE',(0,0),(6,0) , 12),
#     ('FONTSIZE',(0,1),(5,-2) , 10),
#     ('FONTSIZE',(2,1),(3,-1) , 8), # address , problem 
#     ('BOTTOMPADDING',(0,0),(6,0) , 10),
#     ('RIGHTPADDING',(0,0),(6,0) , 10),
#     ('LFETPADDING',(0,0),(6,0) , 10),
#     # ( colWidths=[0.5*inch,0.7*inch,2*inch,2*inch, 1*inch])
#     #('BOX', (0,0), (-1,-1), 0.25, colors.black),
#     ])
#     header = (get_display(arabic_reshaper.reshape(u"کمیسیون")),
#              get_display(arabic_reshaper.reshape(u"اجرت")),
#              get_display(arabic_reshaper.reshape(u"مشکل")),
#              get_display(arabic_reshaper.reshape(u"آدرس")),
#              get_display(arabic_reshaper.reshape(u"شماره سفارش")),
#              get_display(arabic_reshaper.reshape(u"تاریخ")))
#     data=[header]#,(1,2,3,4,5,6),(7,8,9,9,9,9)]

#     agentid  = pk #self.kwargs["pk"]
#     queryset = Lead.objects.filter(status="انجام شد",transaction_status="تسویه نشده",
#     agent__id=agentid
#     ).extra(select={'com': 0}).order_by('-time')
#     for lead in queryset:
#         lead.time = date2jalali(lead.time)
#         com = (0 if lead.total_price_agent is None else lead.total_price_agent)* lead.agent.weight
#         lead.com = int(com)
#         address = get_display(arabic_reshaper.reshape(lead.address))
#         problem = get_display(arabic_reshaper.reshape(lead.problem))
#         row = (f"{lead.com:,}",f"{lead.total_price_agent:,}",problem,address,lead.id,lead.time)
#         data.append(row)
    
#     agent = Agent.objects.get(id=agentid)
#     total_commisions = Transaction.objects.filter(technician__id=agentid,
#     category="دریافتی از سفارش", order__transaction_status="تسویه نشده" )\
#     .aggregate(tot_com = Sum('company_amount'))
#     total_transaction = Transaction.objects.filter(technician__id=agentid,
#     category="دریافتی از سفارش",
#     order__transaction_status="تسویه نشده")\
#     .aggregate(Sum('total_amount'))

#     total_tr = 0 if  total_transaction['total_amount__sum'] is None else total_transaction['total_amount__sum'] 
#     total_com = 0 if total_commisions["tot_com"] is None else int(total_commisions["tot_com"])

#     total_income = get_display(arabic_reshaper.reshape(f"{total_tr:,}" + ' تومان'))
#     total_commision  = get_display(arabic_reshaper.reshape(f"{total_com:,}"  + ' تومان'))
#     data.append((total_commision,total_income,'','','',get_display(arabic_reshaper.reshape(u"جمع کل"))))
    
#     table = Table(data, colWidths=[1.3*inch] * 6, rowHeights=[0.3*inch] * (len(data)))#
#     #colWidth = size * number of columns
#     #rowHeights= size * number of rows
#     table.setStyle(style)
#     elements = []
#     elements.append(table)
    

    
   
#     # doc.build(elements)
#     # doc.showPage()
#     # Close the PDF object cleanly, and we're done.
    



#     ### my code 
#     w ,h = A4

#     # table.wrapOn(c, 10, 10)
#     # table.drawOn(c, 200, 200)
#     table.wrapOn(c, 300, 50)
#     table.drawOn(c, w-580, h-(150+len(data)*20))
    

#     styles = getSampleStyleSheet()    
#     mystyle = ParagraphStyle(name='Right', alignment=TA_RIGHT, fontName='Persian', fontSize=16)

#     p1text = "<b>امداد موتور</b>"
#     p1 = Paragraph(get_display(arabic_reshaper.reshape(p1text)), style=mystyle)
#     p1.wrapOn(c, 200, 50)  # size of 'textbox' for linebreaks etc.
#     p1.drawOn(c, w-450, h-45)

    
#     p2text = "نام کارشناس :  "
#     name = agent.first_name + ' ' + agent.last_name
#     mystyle.fontSize = 11
#     p2 = Paragraph(get_display(arabic_reshaper.reshape(p2text+name)), style=mystyle)
#     p2.wrapOn(c, 200, 50)  # size of 'textbox' for linebreaks etc.
#     p2.drawOn(c, w-250, h-70)


#     p3text = datetime2jalali(datetime.datetime.now()).strftime('%y/%m/%d %H:%M:%S')
#     mystyle.fontSize = 10
#     p3 = Paragraph(get_display(arabic_reshaper.reshape(p3text)), style=mystyle)
#     p3.wrapOn(c, 200, 50)  # size of 'textbox' for linebreaks etc.
#     p3.drawOn(c, w-600, h-70)



#     c.showPage()
#     c.save()

#     # FileResponse sets the Content-Disposition header so that browsers
#     # present the option to save the file.
#     buffer.seek(0)
#     return FileResponse(buffer, as_attachment=True, filename=(name+p3text+'.pdf'))        