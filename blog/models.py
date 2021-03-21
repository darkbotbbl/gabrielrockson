from django.db import models

from wagtail.core.models import Page


class BlogListPage(Page):

    template = "blog_listing.html"

