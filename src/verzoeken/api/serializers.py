import logging

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework.validators import UniqueTogetherValidator
from vng_api_common.serializers import add_choice_values_help_text
from vng_api_common.utils import get_help_text
from vng_api_common.validators import (
    IsImmutableValidator,
    ResourceValidator,
    UniekeIdentificatieValidator,
)

from verzoeken.api.auth import get_auth
from verzoeken.datamodel.constants import (
    IndicatieMachtiging,
    KlantRol,
    ObjectTypes,
    VerzoekStatus,
)
from verzoeken.datamodel.models import (
    KlantVerzoek,
    ObjectVerzoek,
    Verzoek,
    VerzoekContactMoment,
    VerzoekInformatieObject,
    VerzoekProduct,
)
from verzoeken.sync.signals import SyncError

from .validators import ObjectVerzoekCreateValidator

logger = logging.getLogger(__name__)


class VerzoekSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Verzoek
        fields = (
            "url",
            "identificatie",
            "bronorganisatie",
            "externe_identificatie",
            "registratiedatum",
            "voorkeurskanaal",
            "tekst",
            "status",
            "in_te_trekken_verzoek",
            "intrekkende_verzoek",
            "aangevulde_verzoek",
            "aanvullende_verzoek",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "identificatie": {"validators": [IsImmutableValidator()]},
            "in_te_trekken_verzoek": {"lookup_field": "uuid"},
            "intrekkende_verzoek": {"lookup_field": "uuid", "read_only": True,},
            "aangevulde_verzoek": {"lookup_field": "uuid"},
            "aanvullende_verzoek": {"lookup_field": "uuid", "read_only": True,},
        }
        # Replace a default "unique together" constraint.
        validators = [UniekeIdentificatieValidator("bronorganisatie", "identificatie")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(VerzoekStatus)
        self.fields["status"].help_text += f"\n\n{value_display_mapping}"


class ObjectVerzoekSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ObjectVerzoek
        fields = ("url", "verzoek", "object", "object_type")
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "verzoek": {
                "lookup_field": "uuid",
                "validators": [IsImmutableValidator()],
            },
            "object": {"validators": [IsImmutableValidator()],},
            "object_type": {"validators": [IsImmutableValidator()]},
        }
        validators = [ObjectVerzoekCreateValidator()]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(ObjectTypes)
        self.fields["object_type"].help_text += f"\n\n{value_display_mapping}"

        if not hasattr(self, "initial_data"):
            return


class VerzoekInformatieObjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VerzoekInformatieObject
        fields = ("url", "informatieobject", "verzoek")
        validators = [
            UniqueTogetherValidator(
                queryset=VerzoekInformatieObject.objects.all(),
                fields=["verzoek", "informatieobject"],
            ),
        ]
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "informatieobject": {
                "validators": [
                    ResourceValidator(
                        "EnkelvoudigInformatieObject",
                        settings.DRC_API_SPEC,
                        get_auth=get_auth,
                    ),
                    IsImmutableValidator(),
                ]
            },
            "verzoek": {"lookup_field": "uuid", "validators": [IsImmutableValidator()]},
        }

    def save(self, **kwargs):
        # can't slap a transaction atomic on this, since DRC/verzoeken query for the
        # relation!
        try:
            return super().save(**kwargs)
        except SyncError as sync_error:
            # delete the object again
            VerzoekInformatieObject.objects.filter(
                informatieobject=self.validated_data["informatieobject"],
                verzoek=self.validated_data["verzoek"],
            )._raw_delete("default")
            raise serializers.ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: sync_error.args[0]}
            ) from sync_error


class VerzoekContactMomentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VerzoekContactMoment
        fields = ("url", "contactmoment", "verzoek")
        validators = [
            UniqueTogetherValidator(
                queryset=VerzoekContactMoment.objects.all(),
                fields=["verzoek", "contactmoment"],
            ),
        ]
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "verzoek": {"lookup_field": "uuid", "validators": [IsImmutableValidator()]},
            "contactmoment": {"validators": [IsImmutableValidator()]},
        }


class ProductSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=20,
        source="product_code",
        help_text=get_help_text("datamodel.VerzoekProduct", "product_code"),
    )


class VerzoekProductSerializer(serializers.HyperlinkedModelSerializer):
    product_identificatie = ProductSerializer(
        source="*",
        required=False,
        allow_null=True,
        help_text=_(
            "Identificerende gegevens van het PRODUCT voor het geval er bij `product` "
            "geen URL kan worden opgenomen naar het PRODUCT in de Producten en "
            "Diensten API."
        ),
    )

    class Meta:
        model = VerzoekProduct
        fields = ("url", "verzoek", "product", "product_identificatie")
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "verzoek": {
                "lookup_field": "uuid",
                "validators": [IsImmutableValidator(),],
            },
            "product": {"validators": [IsImmutableValidator(),],},
        }

    def validate(self, attrs):
        validated_attrs = super().validate(attrs)
        product = validated_attrs.get("product", None)
        product_code = validated_attrs.get("product_code", None)

        if not product and not product_code:
            raise serializers.ValidationError(
                _("product or productIdentificatie must be provided"),
                code="invalid-product",
            )

        return validated_attrs


class KlantVerzoekSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KlantVerzoek
        fields = ("url", "klant", "verzoek", "rol", "indicatie_machtiging")
        validators = [
            UniqueTogetherValidator(
                queryset=KlantVerzoek.objects.all(), fields=["verzoek", "klant"],
            ),
        ]
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "verzoek": {"lookup_field": "uuid", "validators": [IsImmutableValidator()]},
            "klant": {"validators": [IsImmutableValidator()]},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        rol_machtiging_display_mapping = add_choice_values_help_text(KlantRol)
        self.fields["rol"].help_text += f"\n\n{rol_machtiging_display_mapping}"

        indicatie_machtiging_display_mapping = add_choice_values_help_text(
            IndicatieMachtiging
        )
        self.fields[
            "indicatie_machtiging"
        ].help_text += f"\n\n{indicatie_machtiging_display_mapping}"
