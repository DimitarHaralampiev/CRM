from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from leads.forms import LeadModelForm
from leads.models import Lead


class SignupView(LoginRequiredMixin, CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')


class LandingPageView(LoginRequiredMixin, TemplateView):
    template_name = 'landing.html'


def landing_page(request):
    return render(request, 'landing.html')


class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'leads/lead_list.html'
    queryset = Lead.objects.all()
    context_object_name = 'leads'


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request, 'leads/lead_list.html', context)


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_details.html'
    queryset = Lead.objects.all()
    context_object_name = 'lead'


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead': lead
    }
    return render(request, 'leads/lead_details.html', context)


class LeadCreateView(LoginRequiredMixin, CreateView):
    template_name = 'leads/lead_create.html'
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        send_mail(
            subject='A lead has been created',
            message='Go to the site to see the new lead',
            from_email='test@test.com',
            recipient_list=['test2@test.com']
        )
        return reverse('leads:lead-list')

    def form_valid(self, form):
        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    form = LeadModelForm()
    if request.POST == 'POST':
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        'form': form
    }
    return render(request, 'leads/lead_create.html', context)


class LeadUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-update')


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm()
    if request.POST == 'POST':
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            lead.save()
            return redirect('/leads')
    context = {
        'form': form,
        'lead': lead
    }
    return render(request, 'leads/lead_update.html', context)


class LeadDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:lead-list')


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')

# def lead_create(request):
#     form = LeadForm()
#     if request.POST == 'POST':
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             Lead.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 agent=agent
#             )
#             return redirect('/leads')
#     context = {
#         'form': form
#     }
#     return render(request, 'leads/lead_create.html.', context)
