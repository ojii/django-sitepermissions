from django.core.exceptions import NON_FIELD_ERRORS
from django.forms.util import ErrorDict


class V(object):
    """
    A validator object (similar to the ORM's Q object) with the ability to OR
    and AND.
    
    Eg:
    
    V(some_validator(...)) | V(some_other_validator(...))
    """
    def __init__(self, validator):
        self.validator = validator
        self.added = False
        self.or_validators = []
        self.and_validators = []
        
    def __or__(self, other):
        if not self.added:
            self.or_validators.append(self.validator)
            self.added = True
        self.or_validators.append(other)
        return self
        
    def __and__(self, other):
        if not self.added:
            self.and_validators.append(self.validator)
            self.added = True
        self.and_validators.append(other)
        return self
        
    def __call__(self, admin, request, form, **data):
        if not self.added:
            return self.validator(admin, request, form, **data)
        if form._errors is None:
            frozenerrors = ErrorDict()
        else:
            frozenerrors = form._errors.copy()
        frozendata = form.cleaned_data.copy()
        or_validators = self.or_validators
        if not any([v(admin, request, form, **data) for v in self.or_validators]):
            return False
        form._errors = frozenerrors
        form.cleaned_data = frozendata
        return all([v(admin, request, form, **data) for v in self.and_validators])


def m2m_validator(fieldname):
    """
    Validates a M2M to the sites.Site model using 'fieldname'
    """
    def validate_form(admin, request, form, **data):
        user = request.user
        sites = data[fieldname]
        for site in sites:
            if not user.groups.filter(sitegroup__sites=site).count():
                return form.invalid_form(sites=["You do not have the rights to add news for this site: %s" % site])
        return True
    return validate_form

def superuser_validator(*validators):
    """
    Validates if the user is a superuser, alternatively uses validators or
    returns False
    """
    validator = multi_validator(*validators)
    def validate_form(admin, request, form, **data):
        if request.user.is_superuser:
            return True
        if validators:
            return validator(admin, request, form, **data)
        return False
    return validate_form

def permission_validator(permcode):
    """
    Validates if a user has a permission.
    """
    def validate_form(admin, request, form, **data):
        if request.user.has_perm(permcode):
            return True
        form.invalid_form(**{NON_FIELD_ERRORS: ["You don't have the required permission: %s" % permcode]})
        return False
    return validate_form

def multi_validator(*validators):
    """
    Simple AND validator for multi_validation
    """
    def validate_form(admin, request, form, **data):
        for validator in validators:
            if not validator(admin, request, form, **data):
                return False
        return True
    return validate_form