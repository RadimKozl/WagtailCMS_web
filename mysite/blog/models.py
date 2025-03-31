"""Blog listing and detail pages."""

from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from streams import blocks

class BlogListingPage(Page):
    """Listing page lists all the Blog Deatail Pages"""
    
    template = "blog/blog_listing_page.html"
    
    custom_title = models.CharField(
        max_length=100, 
        blank=False, 
        null=False,
        help_text="Overwrite the default title", 
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
    ]
    
    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all BlogDetailPage instances
        context['posts'] = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        return context
    
    
class BlogDetailPage(Page):
    """Blog Detail Page"""
    
    template = "blog/blog_detail_page.html"
    
    custom_title = models.CharField(
        max_length=100, 
        blank=False,
        null=False,
        help_text="Overwrite the default title", 
    )
    
    blog_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        related_name='+',
        on_delete=models.SET_NULL, 
    )
    
    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        FieldPanel('blog_image'),
        FieldPanel('content'),
    ]