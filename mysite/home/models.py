from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, PageChooserPanel
#from wagtail.images.edit_handlers import ImageChooserPanel


class HomePage(Page):
    
    max_count = 1
    
    banner_title = models.CharField(
        max_length=100, 
        blank=False, 
        null=True
    )
    
    banner_subtitle = RichTextField(
        features=['bold', 'italic']
    )
    
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    banner_cta = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('banner_title'),
        FieldPanel('banner_subtitle'),
        FieldPanel('banner_image'),
        PageChooserPanel('banner_cta')
    ]
    
    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"