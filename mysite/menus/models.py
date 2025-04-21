"""Menus models."""
from django.db import models

from django_extensions.db.fields import AutoSlugField

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.models import Orderable
from wagtail.admin.panels import (
    FieldPanel, 
    MultiFieldPanel, 
    InlinePanel
)

from wagtail.snippets.models import register_snippet

class MenuItem(Orderable):
    """Menus models."""
    link_title = models.CharField(
        blank=True,
        null=True,
        max_length=50
    )
    link_url = models.CharField(
        blank=True,
        max_length=500  
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.CASCADE
    )
    open_in_new_tab = models.BooleanField(default=False, blank=True)

    page = ParentalKey("Menu", related_name="menu_items")
    
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("link_title"),
                FieldPanel("link_url"),
                FieldPanel("link_page"),
                FieldPanel("open_in_new_tab"),
            ], heading="Menu Item"
        ),
    ]
    
    @property
    def link(self):
        """Return the link URL or page URL."""
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'
    
    
    @property
    def title(self):
        """Return the link title."""
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return 'Missing Title'
    
@register_snippet
class Menu(ClusterableModel):
    """The main menu clusterable model."""
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', editable=True)
    # slug = models.SlugField(max_length=100, unique=True, editable=False)
    
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("slug"),
            ], heading="Menu"
        ), 
        InlinePanel("menu_items", label="Menu Items"),
    ]
    
    def __str__(self):
        return self.title
    
