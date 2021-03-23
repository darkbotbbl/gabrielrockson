from django.db import models
import blog

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import RichTextFieldPanel, FieldPanel
from wagtail.search import index


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
    ]