from django.contrib import messages
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView
from django import forms
from django.shortcuts import redirect
from .mixins import WizardConfirmationMixin
from ..forms import FooForm, BarForm, FooConfirmationForm, BarConfirmationForm

MIXIN_DEMO_WIZARD_STEP_URL_NAME = "demo-wizard-step"
MIXIN_DEMO_WIZARD_DONE_URL_NAME = "demo-wizard-done"

named_order_forms = (
    ("foo", FooForm),
    ("confirm-foo", FooConfirmationForm),
    ("bar", BarForm),
    ("confirm-bar", BarConfirmationForm),
)

class MixinDemoWizard(WizardConfirmationMixin, NamedUrlSessionWizardView):
    template_name = "django_formwizard_mixins/wizard.html"
    
    def done(self, form_list, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, 'Done!')
        return redirect(MIXIN_DEMO_WIZARD_DONE_URL_NAME)

mixin_demo_wizard_view = MixinDemoWizard.as_view(
    named_order_forms,
    url_name=MIXIN_DEMO_WIZARD_STEP_URL_NAME,
    done_step_name=MIXIN_DEMO_WIZARD_DONE_URL_NAME,
)