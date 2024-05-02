from django.contrib.auth.mixins import UserPassesTestMixin


class AccountManagerRequiredMixin(UserPassesTestMixin):
    def __init__(self):
        self.request = None

    def test_func(self):
        user = self.request.user

        """ Debug print: Print the request user's username
        #print(f"Request user: {user.email}") """

        # Debug print: Print the groups the user belongs to
        # groups = user.groups.all()
        # group_names = [group.name for group in groups]
        # print("User belongs to groups:", group_names)

        # Check if the user is in the "Account Managers" group
        is_account_manager = user.groups.filter(name="Account Managers").exists()

        """ Debug print: Print the result of the group check
        print(f"Is user an Account Manager? {is_account_manager}") """

        return is_account_manager
