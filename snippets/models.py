"""This module has the snippets used on the page"""
from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField


# Snippet used to add blog categories 
@register_snippet
class BlogCategory(models.Model):
    """This model is used to create a blog category independent of a blog page"""
    name = models.CharField(max_length=50, blank=False, null=False)
    icon = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name_plural = "Blog Categories"

    panels = [
        FieldPanel("name"),
        ImageChooserPanel("icon")
    ]


# Snippet for blog author
@register_snippet
class BlogAuthor(models.Model):
    """This is a model that represents an author of a blog"""
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    avatar = models.ForeignKey(
        "wagtailimages.Image",
        related_name="+",
        blank=False,
        null=False,
    )
    phone = models.PositiveIntegerField()
    email = models.EmailField(blank=False, null=False)
    twitter_handle = models.URLField(blank=True, null=True, help_text="Enter the link to your twitter handle")
    facebook = models.URLField(blank=True, null=True, help_text="Enter the link to your facebook account")
    instagram = models.URLField(blank=True, null=True, help_text="Enter the link to your instagram account")

    panels = [
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        ImageChooserPanel("avatar"),
        FieldPanel("email"),
        FieldPanel("twitter_handle"),
        FieldPanel("facebook"),
        FieldPanel("instagram"),
    ]