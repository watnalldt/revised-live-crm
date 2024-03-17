from django.urls import reverse
from django.test import RequestFactory
from pages.views import HomePageView, MarketUpdateView, SeamlessUtilitiesView, PartnersView


class BasePageViewTest:
    def setup_method(self):
        self.factory = RequestFactory()

    def get_response(self, url_name):
        request = self.factory.get(reverse(url_name))
        return self.view_class.as_view()(request)

    def test_view_uses_correct_template(self):
        response = self.get_response(self.url_name)
        assert f"pages/{self.template_name}" in response.template_name

    def test_view_html_title(self):
        response = self.get_response(self.url_name)
        assert "html_title" in response.context_data
        assert response.context_data["html_title"] == self.expected_title


class TestHomePageView(BasePageViewTest):
    def setup_method(self):
        super().setup_method()
        self.view_class = HomePageView
        self.url_name = "pages:home"
        self.template_name = "index.html"
        self.expected_title = "Effectively Managing Energy Solutions"


class TestMarketUpdateView(BasePageViewTest):
    def setup_method(self):
        super().setup_method()
        self.view_class = MarketUpdateView
        self.url_name = "pages:market_update"
        self.template_name = "market_update.html"
        self.expected_title = "Energy Portfolio Market Update"


class TestSeamlessUtilitiesView(BasePageViewTest):
    def setup_method(self):
        super().setup_method()
        self.view_class = SeamlessUtilitiesView
        self.url_name = "pages:seamless_utilities"
        self.template_name = "seamless_utilities.html"
        self.expected_title = "Energy Portfolio Seamless Utilities"


class TestPartnersView(BasePageViewTest):
    def setup_method(self):
        super().setup_method()
        self.view_class = PartnersView
        self.url_name = "pages:partners"
        self.template_name = "our_partners.html"
        self.expected_title = "Energy Portfolio Our Partners"
