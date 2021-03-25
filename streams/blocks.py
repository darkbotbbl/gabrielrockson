"""This module contains blocks that will be used for custom StreamFields"""
from django.db import models
from wagtail.core import blocks


class TitleBlock(blocks.CharBlock):
    """This block adds a heading"""

    class Meta:
        icon = "title"
        template = "title_block.html"


class NormalTextBlock(blocks.TextBlock):
    """This block adds a normal text to the page without any editing features"""

    class Meta:
        icon = "placeholder"
        label = "Normal Text Field"
        template = "normal_text_block.html"


class FullRichTextFieldBlock(blocks.RichTextBlock):
    """This blocks enables the user to get a fully blown rich text editor"""

    class Meta:
        template = "full_rich_text_field_block.html"
        label = "Full RichText Field"