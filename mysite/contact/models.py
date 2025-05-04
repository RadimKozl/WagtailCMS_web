from django.db import models
from django import forms

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel
)
from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import (
    AbstractEmailForm, 
    AbstractFormField
)

from wagtailcaptcha.models import WagtailCaptchaEmailForm

class FormField(AbstractFormField):
    """A field in a Contact form"""
    page = ParentalKey(
        'ContactPage', 
        on_delete=models.CASCADE, 
        related_name='form_fields'
    )
    

class ContactPage(WagtailCaptchaEmailForm):
    """A page that contains a Contact form"""
    
    template = 'contact/contact_page.html'
    # This is the default path
    # If ignored, Waigtail adds _landing.html to your template name
    landing_page_template = 'contact/contact_page_landing.html'
    
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form Fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
                FieldRowPanel([
                    FieldPanel('from_address', classname="col6"),
                    FieldPanel('to_address', classname="col6"),
                ]),
                FieldPanel('subject'),
            ], heading="Email Settings"),
    
    ]
    
    def serve(self, request):
        if request.method == 'POST':
            form = self.get_form(request.POST, page=self)

            if form.is_valid():
                self.process_form_submission(form)
                return self.render_landing_page(request, form)
            else:
                return super().serve(request)
        else:
            return super().serve(request)
        
    def get_form_fields(self):
        return self.form_fields.all()
    
   