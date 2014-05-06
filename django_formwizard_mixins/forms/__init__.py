from base import BaseConfirmationForm
from django import forms

class FooForm(forms.Form):
    foo = forms.CharField()

class BarForm(forms.Form):
    bar = forms.CharField()

class DemoConfirmationForm(BaseConfirmationForm):
    def set_forms(self, ordered_form_map):
        super(DemoConfirmationForm, self).set_forms(ordered_form_map)
        
        output = []
        for form in self.ordered_form_map.values():
            if hasattr(form, "cleaned_data"):
                for field in form.cleaned_data:
                    output.append("{0}: {1}".format(field, form.cleaned_data[field]))
        
        self.fields["confirm-%s" % self.__class__.__name__] = forms.BooleanField(help_text=", ".join(output))

class FooConfirmationForm(DemoConfirmationForm):
    pass

class BarConfirmationForm(DemoConfirmationForm):
    pass