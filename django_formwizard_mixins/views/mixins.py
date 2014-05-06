from django import forms
from collections import OrderedDict
from ..forms.base import BaseConfirmationForm

class WizardDynamicFormClassMixin(object):
    def get_form_class(self, step):
        return self.form_list[step]
    
    def get_form(self, step=None, data=None, files=None):
        """
        This method was copied from the base Django 1.6 wizard class in order to
        support a callable `get_form_class` method which allows dynamic modelforms.
        
        Constructs the form for a given `step`. If no `step` is defined, the
        current step will be determined automatically.

        The form will be initialized using the `data` argument to prefill the
        new form. If needed, instance or queryset (for `ModelForm` or
        `ModelFormSet`) will be added too.
        """
        if step is None:
            step = self.steps.current
        form_cls = self.get_form_class(step)
        # prepare the kwargs for the form instance.
        kwargs = self.get_form_kwargs(step)
        kwargs.update({
            'data': data,
            'files': files,
            'prefix': self.get_form_prefix(step, form_cls),
            'initial': self.get_form_initial(step),
        })
        if issubclass(form_cls, forms.ModelForm):
            # If the form is based on ModelForm, add instance if available
            # and not previously set.
            kwargs.setdefault('instance', self.get_form_instance(step))
        elif issubclass(form_cls, forms.models.BaseModelFormSet):
            # If the form is based on ModelFormSet, add queryset if available
            # and not previous set.
            kwargs.setdefault('queryset', self.get_form_instance(step))
        return form_cls(**kwargs)

class WizardConfirmationMixin(WizardDynamicFormClassMixin):
    """
        This wizard mixin allows for confirmation forms being
        placed arbitrarily in the form_list.  The confirmation
        forms must subclass the BaseConfirmationForm class in
        order to be detected as a confirmation form.  Each
        confirmation form will be provided with all forms that
        come before it in the form_list so that the confirmation
        page can include the data the user is confirming.  The
        form_list must not contain two confirmation forms of the
        same class or the detection is ambiguous.
    """
    def get_form(self, **kwargs):
        form = super(WizardConfirmationMixin, self).get_form(**kwargs)
        
        if isinstance(form, BaseConfirmationForm):
            form.set_forms(**self.get_set_forms_kwargs(form))
        
        return form
    
    def get_set_forms_kwargs(self, form):
        return {"ordered_form_map": self.get_ordered_form_map(form)}
    
    def get_ordered_form_map(self, form):
        ordered_form_map = OrderedDict()
        
        for form_key in self.get_form_list():
            form_cls = self.get_form_class(form_key)
            if issubclass(form_cls, BaseConfirmationForm) and isinstance(form, form_cls):
                # this allows arbitrary placement of confirmation forms in the
                # form_list. breaking like this provides the confirmation form
                # with all forms that come before it, but not the ones after it.
                break
                   
            form_obj = self.get_form(step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            
            # required to set instance on model forms
            form_obj.is_valid()
            
            ordered_form_map[form_key] = form_obj
        
        return ordered_form_map
    
    def render(self, form=None, **kwargs):
        form = form or self.get_form()
        
        if isinstance(form, BaseConfirmationForm):
            # do not allow users to confirm invalid data 
            for form_key, form_obj in form.ordered_form_map.iteritems():
                if not form_obj.is_valid():
                    return self.render_revalidation_failure(form_key, form_obj, **kwargs)
        
        return super(WizardConfirmationMixin, self).render(form=form, **kwargs)