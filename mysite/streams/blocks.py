"""StreamFields live in here."""

from wagtail import blocks

class TitleAndTextBlock(blocks.StructBlock):
    """Title and text and nothing else."""
    title = blocks.CharBlock(required=True, help_text="Add your title")
    text = blocks.TextBlock(required=True, help_text="Add additional text")

    class Meta:  #noqa
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"
        

class RichTextBlock(blocks.RichTextBlock):
    """Richtext with all the features."""
    
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