"""Blog listing and detail pages."""

from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.admin.panels import (
    FieldPanel, 
    MultiFieldPanel, 
    InlinePanel
)
from wagtail.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, re_path
from wagtail.snippets.models import register_snippet

from streams import blocks

class BlogAuthorsOrderable(Orderable):
    """This allow us to select one or more authors from Snippets."""
    page = ParentalKey("blog.BlogDetailPage", related_name="blog_authors")
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,
    )
    
    panels = [
        FieldPanel('author'),
    ]

class BlogAuthor(models.Model):
    """Blog author for snippets."""
    
    name = models.CharField(max_length=100, blank=False, null=False)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        related_name='+',
        on_delete=models.SET_NULL, 
    )
    
    panels = [
        MultiFieldPanel(
            [
                FieldPanel('name'),
                FieldPanel('image'),
            ],
            heading="Name and Image",
        ),
        MultiFieldPanel(
            [
                FieldPanel('website'),
            ],
            heading="Links",
        )
    ]
    def __str__(self):
        """String repr of this class"""
        return self.name
    
    class Meta:
        """Meta class."""
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"
        
register_snippet(BlogAuthor)

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
        #context['a_special_link'] = self.reverse_subpage('latest_posts')
        context['authors'] = BlogAuthor.objects.all()
        return context
    
    @re_path(r'^latest/$', name='latest_posts')
    def latest_blog_posts(self, request, *args, **kwargs):
        """Get latest blog posts."""
        context = self.get_context(request, *args, **kwargs)
        context['latest_posts'] = BlogDetailPage.objects.live().public()[:1]  # Get the latest post
        return render(request, 'blog/latest_posts.html', context)
    
    def get_sitemap_urls(self, request):
        """Get sitemap urls."""
        # Uncoment to have no sitemap for this page
        # return []
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                'location': self.full_url + self.reverse_subpage('latest_posts'),
                'lastmod': (self.last_published_at or self.latest_revision.created_at),
                'priority': 0.9,
            }
        )
        
        return sitemap
    
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
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label="Author", min_num=1, max_num=4),
            ],
            heading="Author(s)",
        ),
        FieldPanel('content'),
    ]