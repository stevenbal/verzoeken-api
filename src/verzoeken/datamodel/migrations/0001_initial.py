# Generated by Django 2.2.11 on 2020-05-20 13:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid
import vng_api_common.fields
import vng_api_common.models
import vng_api_common.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Verzoek",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        help_text="Unieke resource identifier (UUID4)",
                        unique=True,
                    ),
                ),
                (
                    "bronorganisatie",
                    vng_api_common.fields.RSINField(
                        help_text="Het RSIN van de Niet-natuurlijk persoon zijnde de organisatie die de klantinteractie heeft gecreeerd. Dit moet een geldig RSIN zijn van 9 nummers en voldoen aan https://nl.wikipedia.org/wiki/Burgerservicenummer#11-proef",
                        max_length=9,
                    ),
                ),
                (
                    "klant",
                    models.URLField(
                        blank=True,
                        help_text="URL-referentie naar een KLANT (in Klanten API)",
                        max_length=1000,
                    ),
                ),
                (
                    "interactiedatum",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="De datum en het tijdstip waarop de klantinteractie heeft plaatsgevonden.",
                    ),
                ),
                (
                    "tekst",
                    models.TextField(
                        blank=True,
                        help_text="Een toelichting die inhoudelijk de klantinteractie van de klant beschrijft.",
                    ),
                ),
                (
                    "voorkeurskanaal",
                    models.CharField(
                        blank=True,
                        help_text="Het communicatiekanaal dat voor opvolging van de klantinteractie de voorkeur heeft van de KLANT.",
                        max_length=50,
                    ),
                ),
                (
                    "identificatie",
                    models.CharField(
                        blank=True,
                        help_text="De unieke identificatie van het VERZOEK binnen de organisatie die verantwoordelijk is voor de behandeling van het VERZOEK.",
                        max_length=40,
                        validators=[
                            vng_api_common.validators.AlphanumericExcludingDiacritic()
                        ],
                    ),
                ),
                (
                    "externe_identificatie",
                    models.CharField(
                        blank=True,
                        help_text="De identificatie van het VERZOEK buiten de eigen organisatie.",
                        max_length=40,
                        validators=[
                            vng_api_common.validators.AlphanumericExcludingDiacritic()
                        ],
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ontvangen", "Ontvangen"),
                            ("in_behandeling", "In behandeling"),
                            ("afgehandeld", "Afgehandeld"),
                            ("afgewezen", "Afgewezen"),
                            ("ingetrokken", "Ingetrokken"),
                        ],
                        help_text="De waarden van de typering van de voortgang van afhandeling van een VERZOEK.",
                        max_length=20,
                    ),
                ),
            ],
            options={
                "verbose_name": "verzoek",
                "verbose_name_plural": "verzoeken",
                "unique_together": {("bronorganisatie", "identificatie")},
            },
            bases=(vng_api_common.models.APIMixin, models.Model),
        ),
        migrations.CreateModel(
            name="VerzoekProduct",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        help_text="Unieke resource identifier (UUID4)",
                        unique=True,
                    ),
                ),
                (
                    "product",
                    models.URLField(
                        blank=True,
                        help_text="URL-referentie naar het PRODUCT (in de Producten en Diensten API).",
                    ),
                ),
                (
                    "product_code",
                    models.CharField(
                        blank=True,
                        help_text="De unieke code van het PRODUCT.",
                        max_length=20,
                    ),
                ),
                (
                    "verzoek",
                    models.ForeignKey(
                        help_text="URL-referentie naar het VERZOEK.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamodel.Verzoek",
                    ),
                ),
            ],
            bases=(vng_api_common.models.APIMixin, models.Model),
        ),
        migrations.CreateModel(
            name="VerzoekInformatieObject",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        help_text="Unieke resource identifier (UUID4)",
                        unique=True,
                    ),
                ),
                (
                    "informatieobject",
                    models.URLField(
                        help_text="URL-referentie naar het INFORMATIEOBJECT (in de Documenten API) waarin (een deel van) het verzoek beschreven is of aanvullende informatie biedt bij het VERZOEK.",
                        max_length=1000,
                        verbose_name="informatieobject",
                    ),
                ),
                (
                    "verzoek",
                    models.ForeignKey(
                        help_text="URL-referentie naar het VERZOEK.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamodel.Verzoek",
                    ),
                ),
            ],
            options={
                "verbose_name": "verzoekinformatieobject",
                "verbose_name_plural": "verzoekinformatieobjecten",
                "unique_together": {("verzoek", "informatieobject")},
            },
        ),
        migrations.CreateModel(
            name="VerzoekContactMoment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        help_text="Unieke resource identifier (UUID4)",
                        unique=True,
                    ),
                ),
                (
                    "contactmoment",
                    models.URLField(
                        help_text="URL-referentie naar een CONTACTMOMENT (in Contactmoment API)",
                        max_length=1000,
                    ),
                ),
                (
                    "verzoek",
                    models.ForeignKey(
                        help_text="URL-referentie naar het VERZOEK.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamodel.Verzoek",
                    ),
                ),
            ],
            options={
                "verbose_name": "verzoekcontactmoment",
                "verbose_name_plural": "verzoekcontactmomenten",
                "unique_together": {("verzoek", "contactmoment")},
            },
        ),
        migrations.CreateModel(
            name="ObjectVerzoek",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        help_text="Unieke resource identifier (UUID4)",
                        unique=True,
                    ),
                ),
                (
                    "object",
                    models.URLField(
                        help_text="URL-referentie naar het gerelateerde OBJECT (in een andere API)."
                    ),
                ),
                (
                    "object_type",
                    models.CharField(
                        choices=[("zaak", "Zaak")],
                        help_text="Het type van het gerelateerde OBJECT.",
                        max_length=100,
                        verbose_name="objecttype",
                    ),
                ),
                (
                    "verzoek",
                    models.ForeignKey(
                        help_text="URL-referentie naar het VERZOEK.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamodel.Verzoek",
                    ),
                ),
            ],
            options={
                "verbose_name": "object-verzoek",
                "verbose_name_plural": "object-verzoeken",
                "unique_together": {("verzoek", "object")},
            },
            bases=(vng_api_common.models.APIMixin, models.Model),
        ),
    ]
