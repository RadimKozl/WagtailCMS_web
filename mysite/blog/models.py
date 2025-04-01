"""Blog listing and detail pages."""

from django.db import models
from django.shortcuts import render

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, path, re_path

from streams import blocks

class BlogListingPage(RoutablePageMixin, Page):
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
        #context['a_special_link'] = self.reverse_subpage('latest_blog_posts')
        return context
    
    @re_path(r'^latest/?$', name='latest_posts')
    def latest_blog_posts(self, request, *args, **kwargs):
        """Get latest blog posts."""
        context = self.get_context(request, *args, **kwargs)
        context['latest_posts'] = BlogDetailPage.objects.live().public()[:1]  # Get the latest post
        return render(request, 'blog/latest_posts.html', context)

    
    
    
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