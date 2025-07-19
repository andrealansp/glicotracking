from django.db import models
from django.utils.text import slugify

class CategoriaTag(models.Model):
    nome = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, editable=False)

    class Meta:
        verbose_name = "Categoria de Tag"
        verbose_name_plural = "Categorias de Tags"
        ordering = ['nome']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Tag(models.Model):
    categoria = models.ForeignKey(CategoriaTag, on_delete=models.CASCADE, related_name="tags")
    nome = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, editable=False)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['nome']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome