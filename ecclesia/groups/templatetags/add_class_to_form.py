from django import template

register = template.Library()

@register.simple_tag
def add_class(form, class_name):
    '''
    Adding class with class_name to all the fields in the form
    '''
    for key in form.fields:
        form.fields[key].widget.attrs["class"] = str(class_name)
    return form
