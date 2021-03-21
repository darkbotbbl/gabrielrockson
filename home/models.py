from django.db import models

from wagtail.core.models import Page


class HomePage(Page):
    
    max_count = 1

    template = "home_page.html"
