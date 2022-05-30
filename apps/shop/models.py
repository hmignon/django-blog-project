import re

from django.core.exceptions import ValidationError
from django.db import models
from django.forms.widgets import RadioSelect
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class ProductPage(Page):
    template = 'shop/product_detail.html'

    # noinspection PyUnresolvedReferences
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    summary = models.CharField(max_length=255, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    in_stock = models.PositiveIntegerField(default=0)
    price_incl_tax = models.FloatField(default=0)
    price_excl_tax = models.FloatField(default=0)
    featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Product Page'
        verbose_name_plural = 'Product pages'

    def save(self, *args, **kwargs):
        self.price_incl_tax = round(self.price_incl_tax, 2)
        self.price_excl_tax = round(self.price_excl_tax, 2)
        super(ProductPage, self).save(*args, **kwargs)

    @property
    def colors(self):
        colors = [
            n.color for n in self.product_color_relationship.all()
        ]
        return colors

    def __str__(self):
        return f"Post #{self.id}: {self.title}"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['owner'] = self.owner

        return context

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('description'),
        index.SearchField('title'),
        index.SearchField('summary')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        ImageChooserPanel('cover_image'),
        FieldPanel('description'),
        InlinePanel('product_color_relationship', heading="Available colors"),
        FieldPanel('featured', widget=RadioSelect(choices=[(True, "Yes"), (False, "No")]),
                   heading="Feature this product on the home page?"),
        InlinePanel('gallery_images', label="Gallery images")
    ]


@register_snippet
class ProductColor(models.Model):
    name = models.CharField(max_length=20)
    hex_code = models.CharField(max_length=7, default="#000000")

    class Meta:
        verbose_name = "Product color"
        verbose_name_plural = "Product colors"

    def __str__(self):
        return self.name

    def clean(self):
        if "#" not in self.hex_code:
            self.hex_code = f"#{self.hex_code}"

        if not re.search(r"^#(?:[\da-fA-F]{3}){1,2}$", self.hex_code):
            raise ValidationError({'hex_code': 'Hex code is invalid.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class ProductColorRelationship(models.Model):
    product = ParentalKey(
        'ProductPage',
        related_name='product_color_relationship'
    )
    color = models.ForeignKey('ProductColor', related_name="+", on_delete=models.CASCADE)

    panels = [
        FieldPanel('color')
    ]


class ProductGalleryImage(Orderable):
    page = ParentalKey('ProductPage', on_delete=models.CASCADE, related_name='gallery_images')
    # noinspection PyUnresolvedReferences
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
