from django import forms

class BaseConfirmationForm(forms.Form):
    @property
    def ordered_form_map(self):
        if self._ordered_form_map is None:
            raise AttributeError("You cannot reference 'ordered_form_map' before calling the 'set_forms' method!")
        return self._ordered_form_map
    _ordered_form_map = None
    
    def set_forms(self, ordered_form_map):
        self._ordered_form_map = ordered_form_map