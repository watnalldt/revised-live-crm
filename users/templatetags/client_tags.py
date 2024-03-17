from datetime import datetime

from django import template

from clients.models import Client
from contracts.models import Contract

register = template.Library()


@register.simple_tag
def total_contracts(user):
    """Returns total number of contracts for a given user."""
    return Contract.objects.filter(client__account_manager=user).count()


@register.simple_tag
def total_clients(user, is_lost=False):
    """
    Returns total number of clients for a given user.
    If is_lost is True, it returns the total number of lost clients.
    Otherwise, it returns the total number of active clients.
    """
    return Client.objects.filter(account_manager=user, is_lost=is_lost).count()


@register.simple_tag
def contracts_by_type(user, contract_type):
    """Returns total number of contracts of a specific type for a given user."""
    return Contract.objects.filter(
        client__account_manager=user, contract_type=contract_type
    ).count()


@register.simple_tag
def directors_approval(user, is_directors_approval):
    """Returns total number of contracts requiring director's approval for a given user."""
    return Contract.objects.filter(
        client__account_manager=user, is_directors_approval=is_directors_approval
    ).count()


@register.simple_tag
def out_of_contract(user, is_ooc):
    """Returns total number of contracts that are out of contract for a given user."""
    return Contract.objects.filter(client__account_manager=user, is_ooc=is_ooc).count()


@register.simple_tag
def contracts_by_utility(user, utility_type):
    """Returns total number of contracts for a specific utility type for a given user."""
    return Contract.objects.filter(
        client__account_manager=user, utility__utility=utility_type
    ).count()


@register.simple_tag
def contracts_by_supplier(user, supplier_name):
    """Returns total number of contracts with a specific supplier for a given user."""
    return Contract.objects.filter(
        client__account_manager=user, supplier__supplier=supplier_name
    ).count()


@register.simple_tag
def contracts_by_status(user, contract_status):
    """Returns total number of contracts with a specific supplier for a given user."""
    return Contract.objects.filter(
        client__account_manager=user, contract_status=contract_status
    ).count()


@register.simple_tag
def expired_contracts(user):
    """Returns total number of contracts that have expired for a given user."""
    # Assuming contract_end_date is a DateTimeField
    end_date = datetime.strptime("01/01/2024", "%d/%m/%Y")
    return Contract.objects.filter(
        client__account_manager=user, contract_end_date__lt=end_date
    ).count()
