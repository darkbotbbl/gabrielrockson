from django.db import models
from django import forms
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class BlogListPage(Page):
    subpage_types = [
        "BlogDetailPage",
    ]
    max_count = 1
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
    tags = ClusterTaggableManager(through="blog.BlogPageTag", blank=True)
    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)
    body = RichTextField()

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    def main_image(self):
        """this method will return the first image in the gallery so it can be used
            as thumbnail image in the listing
        """
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("tags"),
        FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
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


class BlogPageTag(TaggedItemBase):
    """this model is used in creating tags for blog posts"""
    content_object = ParentalKey(BlogDetailPage, on_delete=models.CASCADE, related_name="tagged_items")


class BlogTagsIndexPage(Page):
    """This model is the index blog page of a tag"""

    template = "blog_tags_index_page.html"
    max_count = 1

    def get_context(self, request):
        
        tag = request.GET.get('tag')
        blog_posts = BlogDetailPage.objects.filter(tags__name=tag)

        print(tag)
        print(blog_posts)

        context = super().get_context(request)
        context['blog_posts'] = blog_posts
        context['tag'] = tag
        return context


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