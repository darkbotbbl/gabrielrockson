from django.db import models
import blog

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import InlinePanel, FieldPanel
from wagtail.search import index
from wagtail.images.edit_handlers import ImageChooserPanel


class BlogListPage(Page):
    subpage_types = [
        "BlogDetailPage",
    ]
    template = "blog_listing.html"

    def get_context(self, request):
        context = super().get_context(request)
        blog_posts = self.get_children().live().order_by('-first_published_at')
        context['blog_posts'] = blog_posts
        return context


class BlogDetailPage(Page):
    """This is the model for creating an individual blog post"""
    parent_page_types = [
        BlogListPage
    ]
    template = "blog_detail.html"

    date = models.DateField("Post Date")
    intro = models.CharField("Introduction of the Post", max_length=255)
    body = RichTextField()

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro", classname="full"),
        FieldPanel("body", classname="full"),
        InlinePanel("gallery_images", label="Gallery Images")
    ]



class BlogGallery(Orderable):
    """
        This model is used to add gallery images to a particular blog post
    """
    page = ParentalKey(
        BlogDetailPage,
        on_delete=models.CASCADE,
        related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        related_name="+",
        on_delete=models.CASCADE,
    )
    caption = models.CharField(blank=True, max_length=200)

    panels = [
        ImageChooserPanel("image"),
        FieldPanel("caption"),
    ]