"""StreamFields live in here."""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class TitleAndTextBlock(blocks.StructBlock):
    """Title and text and nothing else."""
    title = blocks.CharBlock(required=True, help_text="Add your title")
    text = blocks.TextBlock(required=True, help_text="Add additional text")

    class Meta:  #noqa
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"
        

class CardBlock(blocks.StructBlock):
    """Cards with image and text and button(s)."""
    title = blocks.CharBlock(required=True, help_text="Add your title")
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                ("button_url", blocks.URLBlock(required=False, help_text="If the button page above is selected, that will be used first.")),
            ]
        )
    )

    class Meta:  #noqa
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Add Cards"

class RichTextBlock(blocks.RichTextBlock):
    """Richtext with all the features."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, features=['h1', 'h2', 'h3', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code', 'center', 'mark'])
    
    class Meta:  #noqa
        template = "streams/rich_text_block.html"
        icon = "doc-full"
        label = "Full RichText"
        

class SimpleRichTextBlock(blocks.RichTextBlock):
    """Richtext without (limited) all the features."""
    
    def __init__(self, required=True, help_text=None, editor='default', features=None, **kwargs): 
        super().__init__(**kwargs)
        self.features = [
            "bold",
            "italic",
            "link",
        ]
        
    class Meta:  #noqa
        template = "streams/rich_text_block.html"
        icon = "edit"
        label = "Simple RichText"
        

class CTABlock(blocks.StructBlock):
    """Simple call to action block."""
    
    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False) # If the button page is selected, this is not used.
    button_text = blocks.CharBlock(required=True, default="Learn More", max_length=40)
    
    class Meta:  #noqa
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"
        
        
class LinkStructValue(blocks.StructValue):
    """Additional logic for our urls."""
    
    def url(self):
        button_page = self.get('button_page')
        external_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif external_url:
            return external_url
        
        return None
    
    # def latest_posts(self):
    #     return BlogDetailPage.objects.live()[:3]


class ButtonBlock(blocks.StructBlock):
    """An external or internal URL."""
    
    button_page = blocks.PageChooserBlock(required=False, help_text="If selected, this url will be use first.")
    button_url = blocks.URLBlock(required=False, help_text="If added, this url will be used secondary ti the buttn page.")
   
    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context['latest_posts'] = BlogDetailPage.objects.live().public()[:3]
        
    #     return context
    
    class Meta:  #noqa
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"
        value_class = LinkStructValue
    