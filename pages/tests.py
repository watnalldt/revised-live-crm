import pytest
from django.urls import reverse
from django.test import RequestFactory
from .views import HomePageView  # Adjust the import path according to your project structure


@pytest.mark.django_db
class TestHomePageView:
    def setup_method(self):
        # Setup RequestFactory to create requests
        self.factory = RequestFactory()

    def test_home_page_view_uses_correct_template(self):
        # Create a request object
        request = self.factory.get(reverse('pages:home'))  # Use the name of the URL pattern for your home page
        # Instantiate the View with our request
        response = HomePageView.as_view()(request)
        # Check if the correct template was used
        assert response.template_name[0] == 'pages/index.html'

    def test_home_page_view_html_title(self):
        request = self.factory.get(reverse('pages:home'))
        response = HomePageView.as_view()(request)
        # HTMLTitleMixin is supposed to set `html_title` in the context,
        # so we check if it's correctly set
        assert 'html_title' in response.context_data
        assert response.context_data['html_title'] == 'Effectively Managing Energy Solutions'
