from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views import generic
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from agents.mixins import *

class SignupView(generic.CreateView):
    template_name='registration/signup.html'
    form_class= CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")


class LandingPageView(TemplateView):
    template_name="landing.html"
    

def landing_page(request):
    return render(request, "landing.html")


class LeadListView(LoginRequiredMixin, ListView):
    template_name='leads/lead_list.html'
    context_object_name='leads' #again contect object name changes to leads

    def get_queryset(self):
        user=self.request.user

        #initial queryset of leads for the entire org
        if user.is_organisor:
            queryset=Lead.objects.filter(organisation=user.userprofile) # here in context lead will be change to object_list
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent  logged in
            queryset=queryset.filter(agent__user=user)
        return queryset

def lead_list(request):
    leads=Lead.objects.all()
    context={
        "leads":leads
    }
    return render(request,"leads/lead_list.html", context)


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name='leads/lead_detail.html'

    def get_queryset(self):
        user=self.request.user

        #initial queryset of leads for the entire org
        if user.is_organisor:
            queryset=Lead.objects.filter(organisation=user.userprofile) # here in context lead will be change to object_list
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent  logged in
            queryset=queryset.filter(agent__user=user)
        return queryset
    
    context_object_name='lead' #again contect object name changes to leads

def lead_detail(request, pk):
    lead=Lead.objects.get(id=pk)
    context={
        "lead":lead
    }
    return render(request, "leads/lead_detail.html",context)


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name='leads/lead_create.html'
    form_class= LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self,form):
        #TODO send mail
        send_mail(
            subject="A lead has been Created", message="Go to the site to see the new lead", from_email="test@test.com", recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)    


def lead_create(request):
    print(request.POST)
    form = LeadModelForm()
    if request.method == "POST":
        form=LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context={
        "form":form,
    }
    return render(request, "leads/lead_create.html", context)


# def lead_create(request):
#     # print(request.POST)
#     form = LeadForm()
#     if request.method == "POST":
#         print("Receiving a post request")
#         form=LeadForm(request.POST)
#         if form.is_valid():
#             print("Form is valid")
#             print(form.cleaned_data)
#             first_name=form.cleaned_data['first_name']
#             last_name=form.cleaned_data['last_name']
#             age=form.cleaned_data['age']
#             agent = Agent.objects.first()
#             Lead.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 agent=agent
#             )
#             print("Lead has been created")
#             return redirect("/leads")
#     context={
#         "form":LeadForm()
#     }
#     return render(request, "leads/lead_create.html", context)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    template_name='leads/lead_update.html'
    form_class= LeadModelForm
    
    def get_queryset(self):
        user=self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

    context_object_name='lead' #again contect object name changes to leads
    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_update(request,pk):
    lead=Lead.objects.get(id=pk)
    form=LeadModelForm(instance=lead)
    if request.method == "POST":
        form=LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context={
        "form":form,
        "lead":lead
    }
    return render(request,"leads/lead_update.html", context)



# def lead_update(request,pk):
#     lead=Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         print("Receiving a post request")
#         form=LeadForm(request.POST)
#         if form.is_valid():
#             first_name=form.cleaned_data['first_name']
#             last_name=form.cleaned_data['last_name']
#             age=form.cleaned_data['age']
#             agent = Agent.objects.first()
#             lead.first_name=first_name
#             lead.last_name=last_name
#             lead.age=age
#             lead.save()
#             return redirect("/leads")
#     context={
#         "form":form,
#         "lead":lead
#     }
#     return render(request, "leads/lead_update.html", context)


class LeadDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name='leads/lead_delete.html'
    
    def get_queryset(self):
        user=self.request.user
        return Lead.objects.filter(organisation=user.userprofile)
    
    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_delete(request,pk):
    lead= Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")