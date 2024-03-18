from django.urls import reverse
from django.test import RequestFactory, TestCase

# Assuming the views are defined as they were originally
from pages.views import HomePageView, MarketUpdateView, SeamlessUtilitiesView


class BasePageViewTest(TestCase):
    view_class = None  # Placeholder, to be defined in subclasses

    def setUp(self):  # Using setUp, which is the conventional setup method in TestCase
        super().setUp()
        self.factory = RequestFactory()

    def get_response(self, url_name):
        """Generate a response for the given url_name."""
        assert self.view_class is not None, "view_class must be defined in the subclass"
        request = self.factory.get(reverse(url_name))
        return self.view_class.as_view()(request)


# Example subclass implementation updated with the necessary attributes and refactored method calls


class TestHomePageView(BasePageViewTest):
    def setUp(self):
        super().setUp()
        self.view_class = HomePageView
        # Now url_name, template_name, and expected_title are just normal class attributes defined in each subclass
        self.url_name = "pages:home"
        self.template_name = "index.html"
        self.expected_title = "Effectively Managing Energy Solutions"

    def test_view_uses_correct_template(self):
        response = self.get_response(self.url_name)
        self.assertIn(f"pages/{self.template_name}", response.template_name)

    def test_view_html_title(self):
        response = self.get_response(self.url_name)
        self.assertIn("html_title", response.context_data)
        self.assertEqual(response.context_data["html_title"], self.expected_title)


class TestMarketUpdateView(BasePageViewTest):
    def setUp(self):
        super().setUp()
        self.view_class = MarketUpdateView
        # Now url_name, template_name, and expected_title are just normal class attributes defined in each subclass
        self.url_name = "pages:market_update"
        self.template_name = "market_update.html"
        self.expected_title = "Energy Portfolio Market Update"

    def test_view_uses_correct_template(self):
        response = self.get_response(self.url_name)
        self.assertIn(f"pages/{self.template_name}", response.template_name)

    def test_view_html_title(self):
        response = self.get_response(self.url_name)
        self.assertIn("html_title", response.context_data)
        self.assertEqual(response.context_data["html_title"], self.expected_title)


class TestSeamlessUtilitiesView(BasePageViewTest):
    def setUp(self):
        super().setUp()
        self.view_class = SeamlessUtilitiesView
        # Now url_name, template_name, and expected_title are just normal class attributes defined in each subclass
        self.url_name = "pages:seamless_utilities"
        self.template_name = "seamless_utilities.html"
        self.expected_title = "Energy Portfolio Seamless Utilities"

    def test_view_uses_correct_template(self):
        response = self.get_response(self.url_name)
        self.assertIn(f"pages/{self.template_name}", response.template_name)

    def test_view_html_title(self):
        response = self.get_response(self.url_name)
        self.assertIn("html_title", response.context_data)
        self.assertEqual(response.context_data["html_title"], self.expected_title)
