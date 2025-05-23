# Generated by Django 5.1.7 on 2025-03-23 22:22

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0003_flex_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flex',
            name='content',
            field=wagtail.fields.StreamField([('title_and_text', 2), ('full_richtext', 3), ('simple_richtext', 4), ('cards', 12), ('cta', 17)], blank=True, block_lookup={0: ('wagtail.blocks.CharBlock', (), {'help_text': 'Add your title', 'required': True}), 1: ('wagtail.blocks.TextBlock', (), {'help_text': 'Add additional text', 'required': True}), 2: ('wagtail.blocks.StructBlock', [[('title', 0), ('text', 1)]], {}), 3: ('streams.blocks.RichTextBlock', (), {}), 4: ('streams.blocks.SimpleRichTextBlock', (), {}), 5: ('wagtail.images.blocks.ImageChooserBlock', (), {'required': True}), 6: ('wagtail.blocks.CharBlock', (), {'max_length': 40, 'required': True}), 7: ('wagtail.blocks.TextBlock', (), {'max_length': 200, 'required': True}), 8: ('wagtail.blocks.PageChooserBlock', (), {'required': False}), 9: ('wagtail.blocks.URLBlock', (), {'help_text': 'If the button page above is selected, that will be used first.', 'required': False}), 10: ('wagtail.blocks.StructBlock', [[('image', 5), ('title', 6), ('text', 7), ('button_page', 8), ('button_url', 9)]], {}), 11: ('wagtail.blocks.ListBlock', (10,), {}), 12: ('wagtail.blocks.StructBlock', [[('title', 0), ('cards', 11)]], {}), 13: ('wagtail.blocks.CharBlock', (), {'max_length': 60, 'required': True}), 14: ('wagtail.blocks.RichTextBlock', (), {'features': ['bold', 'italic'], 'required': True}), 15: ('wagtail.blocks.URLBlock', (), {'required': False}), 16: ('wagtail.blocks.CharBlock', (), {'default': 'Learn More', 'max_length': 40, 'required': True}), 17: ('wagtail.blocks.StructBlock', [[('title', 13), ('text', 14), ('button_page', 8), ('button_url', 15), ('button_text', 16)]], {})}, null=True),
        ),
    ]
