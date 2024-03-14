from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path(
        "seamless-utilities",
        views.SeamlessUtilitiesView.as_view(),
        name="seamless_utilities",
    ),
    path("our-partners", views.PartnersView.as_view(), name="partners"),
    path("our-services", views.OurServicesView.as_view(), name="our_services"),
    path("market-update", views.MarketUpdateView.as_view(), name="market_update"),
    path(
        "complaints-policy",
        views.ComplaintsPolicyView.as_view(),
        name="complaints_policy",
    ),
    path("privacy-policy", views.PrivacyPolicyView.as_view(), name="privacy_policy"),
    path(
        "meter-reading-submission",
        views.meter_reading_submission,
        name="meter_reading_submission",
    ),
    path("contact", views.contact_us, name="contact_us"),
    # path(
    #     "thanks/",
    #     TemplateView.as_view(template_name="pages/thanks.html"),
    #     name="thanks",
    # ),
]
