"""Flexible page."""
from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from streams import blocks

class Flex(Page):
    """Flexible page class."""
    template = "flex/flex_page.html"
    
    subpage_types = ['flex.Flex', 'contact.ContactPage']
    parent_page_types = ['flex.Flex', 'home.HomePage']

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
            ("button", blocks.ButtonBlock()),
        ],
        null=True,
        blank=True
    )

    subtitle = models.CharField(max_length=100, null=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('content'),
    ]
    
    class Meta:
        verbose_name = "Flexible Page"
        verbose_name_plural = "Flexible Pages"
