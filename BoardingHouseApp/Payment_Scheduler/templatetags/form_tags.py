from django import template

register = template.Library()

@register.filter
def get_icon(field_name):
    icons = {
        'username': 'fa-user',
        'password': 'fa-lock',
        'first_name': 'fa-user',
        'last_name': 'fa-user',
        'name': 'fa-user',
        'email': 'fa-envelope',
        'role': 'fa-user-tag',
        'status': 'fa-info-circle',
        'room_number': 'fa-door-open',
        'room_type': 'fa-bed',
        'capacity': 'fa-users',
        'price': 'fa-tag',
        'address': 'fa-map-marker-alt',
        'contact_number': 'fa-phone',
        'parents_name': 'fa-user-friends',
        'parents_contact_number': 'fa-phone',
        'room': 'fa-door-open',
        'due_date': 'fa-calendar-alt',
        'date_left': 'fa-calendar-times',
        'date_entry': 'fa-calendar-check',
        'customer': 'fa-user',
        'amount': 'fa-money-bill-wave',
        'remarks': 'fa-comment-alt',
        'amount_received': 'fa-money-bill',
        'change_amount': 'fa-coins',
        'date_created': 'fa-calendar',
        'date_paid': 'fa-calendar-check',
    }
    return icons.get(field_name, 'fa-pen') # Default icon
