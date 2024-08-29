from unittest.mock import patch
from django.test import TestCase
from ..forms import ContactForm  # Adjust this import based on your project structure


class ContactFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "1234567890",
            "company": "Test Company",
            "message": "This is a test message",
            "captcha": "PASSED",  # This value doesn't matter for testing
        }

    @patch("django_recaptcha.fields.ReCaptchaField.validate")
    def test_valid_form(self, mock_validate):
        form = ContactForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    @patch("django_recaptcha.fields.ReCaptchaField.validate")
    def test_invalid_form_missing_required_fields(self, mock_validate):
        invalid_data = self.valid_data.copy()
        del invalid_data["email"]
        del invalid_data["phone"]
        del invalid_data["message"]
        form = ContactForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("phone", form.errors)
        self.assertIn("message", form.errors)

    @patch("django_recaptcha.fields.ReCaptchaField.validate")
    def test_invalid_email(self, mock_validate):
        invalid_data = self.valid_data.copy()
        invalid_data["email"] = "invalid-email"
        form = ContactForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    @patch("django_recaptcha.fields.ReCaptchaField.validate")
    def test_company_field_optional(self, mock_validate):
        optional_data = self.valid_data.copy()
        del optional_data["company"]
        form = ContactForm(data=optional_data)
        self.assertTrue(form.is_valid())

    @patch("django_recaptcha.fields.ReCaptchaField.validate")
    def test_company_name_google(self, mock_validate):
        invalid_data = self.valid_data.copy()
        invalid_data["company"] = "Google"
        form = ContactForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("company", form.errors)
        self.assertEqual(form.errors["company"][0], "Google cannot be entered as a company name.")

    @patch("django_recaptcha.fields.ReCaptchaField.validate")
    def test_company_name_google_case_insensitive(self, mock_validate):
        invalid_data = self.valid_data.copy()
        invalid_data["company"] = "gOoGlE"
        form = ContactForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("company", form.errors)
        self.assertEqual(form.errors["company"][0], "Google cannot be entered as a company name.")

    @patch("django_recaptcha.fields.ReCaptchaField.validate")
    def test_recaptcha_validation(self, mock_validate):
        form = ContactForm(data=self.valid_data)
        form.is_valid()
        mock_validate.assert_called_once()
