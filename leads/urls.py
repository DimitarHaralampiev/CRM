from django.urls import path

from leads.views import lead_list, lead_detail

app_name = 'leads'

urlpatterns = [
    path('', lead_list),
    path('<pk/>', lead_detail)
]