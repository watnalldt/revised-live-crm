from django.urls import path

from . import views

app_name = "contacts"


urlpatterns = [
    path("", views.ContactListView.as_view(), name="contacts"),
    path("create", views.ContactCreateView.as_view(), name="create_contact"),
    # path('autocomplete-client/', views.ClientAutocomplete.as_view(), name='autocomplete_client'),
    path("edit/<int:pk>/", views.ContactUpdateView.as_view(), name="update_contact"),
    path("create_job_title", views.JobTitleCreateView.as_view(), name="create_job_title"),
]
