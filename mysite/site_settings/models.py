from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting
class SocialMediaSettings(BaseSiteSetting):
    """Social media settings for our custom site."""
    facebook = models.URLField(blank=True, null=True, help_text='Your Facebook profile URL')
    x = models.URLField(blank=True, null=True, help_text='Your X profile URL')
    linkedin = models.URLField(blank=True, null=True, help_text='Your LinkedIn profile URL')
    instagram = models.URLField(blank=True, null=True, help_text='Your Instagram profile URL')
    youtube = models.URLField(blank=True, null=True, help_text='Your YouTube profile URL')
    pinterest = models.URLField(blank=True, null=True, help_text='Your Pinterest profile URL')
    kaggle = models.URLField(blank=True, null=True, help_text='Your Kaggle profile URL')
    github = models.URLField(blank=True, null=True, help_text='Your GitHub profile URL')
    
    panels = [
        MultiFieldPanel([
            FieldPanel('facebook'),
            FieldPanel('x'),
            FieldPanel('linkedin'),
            FieldPanel('instagram'),
            FieldPanel('youtube'),
            FieldPanel('pinterest'),
            FieldPanel('kaggle'),
            FieldPanel('github'),
        ], heading='Social Media Links'),
    ]

    class Meta:
        verbose_name = 'Social Media Settings'
        verbose_name_plural = 'Social Media Settings'
