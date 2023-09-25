from agents.mixins import OrganizorAndLoginRequiredMixin
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from leads.forms import LeadModelForm, AssignAgentForm, LeadCategoryUpdateForm
from leads.models import Lead, Category


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
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organization, agent__isnull=False)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_organisor:
            queryset = Lead.objects.filter(organisation=self.request.user.userprofile, agent__isnull=True)
            context.update({
                'unassigned_leads': queryset
            })
        return context


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request, 'leads/lead_list.html', context)


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_details.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organization)
            queryset = queryset.filter(agent__user=user)
        return queryset


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead': lead
    }
    return render(request, 'leads/lead_details.html', context)


class LeadCreateView(OrganizorAndLoginRequiredMixin, CreateView):
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


class LeadUpdateView(OrganizorAndLoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

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


class LeadDeleteView(OrganizorAndLoginRequiredMixin, DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse('leads:lead-list')


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')


class AssignAgentView(OrganizorAndLoginRequiredMixin, FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super().form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organization)
        context.update({
            'unassigned_lead_count': queryset.filter(category__isnull=True)
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organization)
        return queryset


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/category_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organization)
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_ategory_update.html'
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organization)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse('leads:lead-detail', kwargs={'pk': self.get_object().id})
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
