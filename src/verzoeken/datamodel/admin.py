from django.contrib import admin

from .models import (
    ObjectVerzoek,
    Verzoek,
    VerzoekContactMoment,
    VerzoekInformatieObject,
    VerzoekProduct,
)


@admin.register(Verzoek)
class VerzoekAdmin(admin.ModelAdmin):
    list_display = ["bronorganisatie", "klant", "identificatie", "status"]


@admin.register(ObjectVerzoek)
class ObjectVerzoekAdmin(admin.ModelAdmin):
    list_display = ["verzoek", "object"]


@admin.register(VerzoekInformatieObject)
class VerzoekInformatieObjectAdmin(admin.ModelAdmin):
    list_display = ["verzoek", "informatieobject"]


@admin.register(VerzoekContactMoment)
class VerzoekContactMomentAdmin(admin.ModelAdmin):
    list_display = ["verzoek", "contactmoment"]


@admin.register(VerzoekProduct)
class VerzoekProductAdmin(admin.ModelAdmin):
    list_display = ["verzoek", "product"]
