import random

from django.core.mail import send_mail
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .mixins import OrganisorAndLoginRequiredMixin
from django.shortcuts import reverse

from agents.forms import AgentModelForm
from leads.models import Agent


class AgentListView(OrganisorAndLoginRequiredMixin, ListView):
    template_name = 'agents/agent_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)


class AgentCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizor = False
        user.set_password(f'{random.randint(0, 1000000)}')
        user.save()
        Agent.objects.create(
            user=user,
            organization=self.request.user.userprofile,
        )
        send_mail(
            subject='You are invited to be an agent',
            message='You were added as an agent on CRM. Please come login to start working.',
            from_email='admin@test.com',
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin, DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        Agent.objects.all()


class AgentUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        Agent.objects.all()


class AgentDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = 'agents/agent_delete.html'
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        Agent.objects.all()


