from django import forms
from django.forms.utils import ErrorList

from crits.actors.actor import ActorThreatIdentifier
from crits.campaigns.campaign import Campaign
from crits.core.forms import (
    add_bucketlist_to_form,
    add_ticket_to_form,
    SourceInForm)
from crits.core.handlers import get_item_names
from crits.core import form_consts

from crits.vocabulary.relationships import RelationshipTypes
from crits.vocabulary.acls import Common, ActorACL
relationship_choices = [(c, c) for c in RelationshipTypes.values(sort=True)]

class AddActorForm(SourceInForm):
    """
    Django form for adding an Actor to CRITs.
    """

    error_css_class = 'error'
    required_css_class = 'required'

    name = forms.CharField(label=form_consts.Actor.NAME, required=True)
    aliases = forms.CharField(label=form_consts.Actor.ALIASES, required=False)
    description = forms.CharField(
        label=form_consts.Actor.DESCRIPTION,
        required=False,)
    campaign = forms.ChoiceField(
        widget=forms.Select,
        label=form_consts.Actor.CAMPAIGN,
        required=False)
    confidence = forms.ChoiceField(
        label=form_consts.Actor.CAMPAIGN_CONFIDENCE,
        required=False)
    related_id = forms.CharField(widget=forms.HiddenInput(), required=False, label=form_consts.Common.RELATED_ID)
    related_type = forms.CharField(widget=forms.HiddenInput(), required=False, label=form_consts.Common.RELATED_TYPE)
    relationship_type = forms.ChoiceField(required=False,
                                          label=form_consts.Common.RELATIONSHIP_TYPE,
                                          widget=forms.Select(attrs={'id':'relationship_type'}))

    def __init__(self, username, *args, **kwargs):
        super(AddActorForm, self).__init__(username, *args, **kwargs)

        if username.has_access_to(Common.CAMPAIGN_READ):
            self.fields['campaign'].choices = [('', '')] + [
                (c.name, c.name) for c in get_item_names(Campaign, True)]
        self.fields['confidence'].choices = [
            ('', ''),
            ('low', 'low'),
            ('medium', 'medium'),
            ('high', 'high')]
        self.fields['relationship_type'].choices = relationship_choices
        self.fields['relationship_type'].initial = RelationshipTypes.RELATED_TO

        add_bucketlist_to_form(self)
        add_ticket_to_form(self)

    def clean(self):
        cleaned_data = super(AddActorForm, self).clean()
        campaign = cleaned_data.get('campaign')

        if campaign:
            confidence = cleaned_data.get('confidence')

            if not confidence or confidence == '':
                self._errors.setdefault('confidence', ErrorList())
                self._errors['confidence'].append(u'This field is required if campaign is specified.')

        return cleaned_data


class AddActorIdentifierForm(SourceInForm):
    """
    Django form for adding a new Actor Identifier Type.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    identifier_type = forms.ChoiceField(label="Identifier Type", required=True)
    identifier = forms.CharField(widget=forms.TextInput, required=True)

    def __init__(self, username, *args, **kwargs):
        super(AddActorIdentifierForm, self).__init__(username, *args, **kwargs)

        self.fields['identifier_type'].choices = [
            (c.name, c.name) for c in get_item_names(ActorThreatIdentifier, True)]


class AddActorIdentifierTypeForm(forms.Form):
    """
    Django form for adding a new Actor Identifier Type.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    identifier_type = forms.CharField(widget=forms.TextInput, required=True)

class AttributeIdentifierForm(forms.Form):
    """
    Django form for adding a new Actor Identifier Type.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    # The fields will be populated on-the-fly when the form is
    # rendered so we won't populate them here.
    identifier_type = forms.ChoiceField(label="Identifier Type", required=True)
    identifier = forms.ChoiceField(label="Identifier", required=True)
    confidence = forms.ChoiceField(label="Confidence", required=True)

    def __init__(self, *args, **kwargs):
        super(AttributeIdentifierForm, self).__init__(*args, **kwargs)

        self.fields['confidence'].choices = [
            ('low', 'low'),
            ('medium', 'medium'),
            ('high', 'high')]
