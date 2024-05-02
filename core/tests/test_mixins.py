from django.test import TestCase

from core.views import HTMLTitleMixin


class HTMLTitleMixinTest(TestCase):
    def test_generate_html_title(self):
        # Create an instance of HTMLTitleMixin
        mixin_instance = HTMLTitleMixin()

        # Test with a non-empty title
        mixin_instance.html_title = "Test Title"
        title = mixin_instance.generate_html_title()
        expected_title = "Test Title"
        self.assertEqual(title, expected_title)

        # Test with an empty title and required set to False
        mixin_instance.html_title = ""
        mixin_instance.html_title_required = False
        title = mixin_instance.generate_html_title()
        expected_title = ""
        self.assertEqual(title, expected_title)

        # Test with an empty title and required set to True (raises ValueError)
        mixin_instance.html_title = ""
        mixin_instance.html_title_required = True
        with self.assertRaises(ValueError):
            mixin_instance.generate_html_title()
