from django.template import loader, Context, Library

register = Library()

@register.simple_tag
def bootstrap_form(form):
    template = loader.get_template('core/templatetags/bootstrap_form.html')
    return template.render(Context({'form': form}))
