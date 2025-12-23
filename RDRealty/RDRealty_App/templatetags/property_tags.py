from django import template

register = template.Library()

@register.filter
def get_classification_icon(classification_code):
    icons = {
        'RES': 'fas fa-home',
        'COM': 'fas fa-building',
        'IND': 'fas fa-industry',
        'AGR': 'fas fa-leaf',
        'MIX': 'fas fa-layer-group',
        'INS': 'fas fa-university',
    }
    return icons.get(classification_code, 'fas fa-building')

@register.filter
def get_status_color(status_code):
    colors = {
        'ACT': 'status--active',
        'ACTIVE': 'status--active',
        'COL': 'status--collateral',
        'COLLATERAL': 'status--collateral',
        'SOLD': 'status--sold',
        'SLD': 'status--sold',
        'UND': 'status--under-development',
        'UNDER DEVELOPMENT': 'status--under-development',
        'FORC': 'status--foreclosed',
        'FORECLOSED': 'status--foreclosed',
        'DISP': 'status--disposed',
        'DISPOSED': 'status--disposed',
        'PENT': 'status--pending',
        'PND': 'status--pending',
        'INT': 'status--inactive',
        'INACTIVE': 'status--inactive',
    }
    return colors.get(status_code, 'status--inactive')

@register.filter
def get_status_border(status_code):
    borders = {
        'ACT': 'status-active',
        'ACTIVE': 'status-active',
        'COL': 'status-collateral',
        'COLLATERAL': 'status-collateral',
        'SOLD': 'status-sold',
        'SLD': 'status-sold',
        'UND': 'status-under-dev',
        'UNDER DEVELOPMENT': 'status-under-dev',
        'FORC': 'status-foreclosed',
        'FORECLOSED': 'status-foreclosed',
        'DISP': 'status-disposed',
        'DISPOSED': 'status-disposed',
        'PENT': 'status-pending',
        'PND': 'status-pending',
        'INT': 'status-inactive',
        'INACTIVE': 'status-inactive',
    }
    return borders.get(status_code, 'status-inactive')
