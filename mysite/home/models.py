from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey

from wagtail.api import APIField
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, PageChooserPanel
from wagtail.admin.panels import InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path, re_path


from wagtail.fields import StreamField

from streams import blocks

class HomePageCarouselImage(Orderable):
    """Between 1 and 5 images for the home page carousel"""
    id = models.BigAutoField(primary_key=True)
    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    panels = [
        FieldPanel('carousel_image'),
    ]
    
    api_fields = [
        APIField('carousel_image'),
    ]

class HomePage(RoutablePageMixin, Page):
    """Home page model"""
    
    template = "home/home_page.html"
    subpage_types = [
        'blog.BlogListingPage',
        'contact.ContactPage',
        'flex.Flex',
    ]
    
    parent_page_types = ['wagtailcore.Page']
    
    # max_count = 1
    
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
    
    content = StreamField(
        [
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True
    )
    
    api_fields = [
        APIField('banner_title'),
        APIField('banner_subtitle'),
        APIField('banner_image'),
        APIField('banner_cta'),
        APIField('content'),
        APIField('carousel_images'),
    ]
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('banner_title'),
            FieldPanel('banner_subtitle'),
            FieldPanel('banner_image'),
            PageChooserPanel('banner_cta'),
        ], heading="Banner Options"),
        MultiFieldPanel([
            InlinePanel("carousel_images", max_num=5, min_num=1, label="Image for Carousel"),
        ], heading="Carousel Images"),
        FieldPanel('content'),
    ]
    
    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
    
    
    @re_path(r'^subscribe/$')
    def the_subscribe_path(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return render(request, 'home/subscribe.html', context)
    