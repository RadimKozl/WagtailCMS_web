"""Blog listing and detail pages."""

from django.db import models
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from django.shortcuts import render

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.api import APIField
from wagtail.models import Page, Orderable
from wagtail.admin.panels import (
    FieldPanel, 
    MultiFieldPanel, 
    InlinePanel
)
from wagtail.fields import StreamField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.contrib.routable_page.models import RoutablePageMixin, re_path
from wagtail.snippets.models import register_snippet

from streams import blocks

from rest_framework.fields import Field

class ImageSerializedField(Field):
    """A custom serializer used in Wagtails v2 API."""
    
    def to_representation(self, value):
        """Return the image URL, title and dimensions."""
        if value:
            return {
                "url": value.file.url,
                "title": value.title,
                "width": value.width,
                "height": value.height,
            }
        return None
    
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
    
    @property
    def author_name(self):
        """Get the name of the author."""
        return self.author.name
    
    @property
    def author_website(self):
        """Get the website of the author."""
        return self.author.website
    
    @property
    def author_image(self):
        """Get the image of the author."""
        return self.author.image
    
    api_fields = [
        #APIField('author'),
        APIField('author_name'),
        APIField('author_website'),
        #APIField('author_image', serializer=ImageSerializedField()),
        APIField('image_of_author', serializer=ImageRenditionField('fill-200x250', source="author_image")),
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

class BlogCategory(models.Model):
    """Blog category for snippets."""
    
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(
        verbose_name = "Slug",
        allow_unicode=True,
        max_length = 255,
        help_text="A slug to identify post by this category.",
    )
    
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]
    
    def __str__(self):
        """String repr of this class"""
        return self.name
    
    class Meta:
        """Meta class."""
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ['name']

register_snippet(BlogCategory)

class BlogListingPage(RoutablePageMixin, Page):
    """Listing page lists all the Blog Deatail Pages"""
    
    template = "blog/blog_listing_page.html"
    ajax_template = "blog/blog_listing_page_ajax.html"
    max_count = 1
    subpage_types = ['blog.BlogDetailPage','blog.ArticleBlogPage','blog.VideoBlogPage']

    
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
        #context['posts'] = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        paginator = Paginator(all_posts, 3)  # @todo change to 5 per page
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
            
        context['posts'] = posts
        #context['a_special_link'] = self.reverse_subpage('latest_posts')
        context["categories"] = BlogCategory.objects.all()
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
    """Parental Blog Detail Page"""
    
    template = "blog/blog_detail_page.html"
    
    subpage_types = []
    parent_page_types = ['blog.BlogListingPage']
    
    custom_title = models.CharField(
        max_length=100, 
        blank=False,
        null=False,
        help_text="Overwrite the default title", 
    )
    
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        related_name='+',
        on_delete=models.SET_NULL, 
    )
    
    categories = ParentalManyToManyField(
        'blog.BlogCategory',
        blank=True,
        related_name='blog_categories',
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
        FieldPanel('banner_image'),
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label="Author", min_num=1, max_num=4),
            ],
            heading="Author(s)",
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
            ],
            heading="Categories",
        ),
        FieldPanel('content'),
    ]
    
    api_fields = [
        APIField('blog_authors'),
        APIField('content'),
    ]
    
    def save(self, *args, **kwargs):
        """Create a template fragment key for this page.
        Then delete  the key from the cache."""
        # Clear the cache for this page
        key = make_template_fragment_key(
            "blog_post_preview",
            [self.id]
        )
        cache.delete(key)
        return super().save(*args, **kwargs)


    
# First subclassed blog post page
class ArticleBlogPage(BlogDetailPage):
    """A subclassed blog post page for articles."""
    
    template = "blog/article_blog_page.html"
    
    subtitle = models.CharField(
        max_length=100, 
        blank=True,
        null=True 
    )
    
    intro_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Best size for this image will be 1400x400px",
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        FieldPanel('subtitle'),
        FieldPanel('banner_image'),
        FieldPanel('intro_image'),
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label="Author", min_num=1, max_num=4),
            ],
            heading="Author(s)",
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
            ],
            heading="Categories",
        ),
        FieldPanel('content'),
    ]
    
    
# Second subclassed blog post page
class VideoBlogPage(BlogDetailPage):
    """A video subclassed page."""
    
    template = "blog/video_blog_page.html"
    
    youtube_video_id = models.CharField(max_length=30, blank=True, null=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        FieldPanel('banner_image'),
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label="Author", min_num=1, max_num=4),
            ],
            heading="Author(s)",
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
            ],
            heading="Categories",
        ),
        FieldPanel('youtube_video_id'),
        FieldPanel('content'),
    ]   
    