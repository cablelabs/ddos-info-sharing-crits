from django import forms
from django.forms.utils import ErrorList

from crits.campaigns.campaign import Campaign
from crits.core.forms import add_bucketlist_to_form, add_ticket_to_form, SourceInForm
from crits.core.handlers import get_item_names, get_source_names
from crits.core.user_tools import get_user_organization
from crits.core import form_consts

from crits.vocabulary.ips import IPTypes
from crits.vocabulary.relationships import RelationshipTypes
from crits.vocabulary.acls import Common, IPACL

relationship_choices = [(c, c) for c in RelationshipTypes.values(sort=True)]
ip_choices = [(c,c) for c in IPTypes.values(sort=True)]

class AddIPForm(SourceInForm):
    """
    Django form for adding an IP to CRITs.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    ip = forms.CharField(required=True,
                         label=form_consts.IP.IP_ADDRESS,
                         widget=forms.TextInput(attrs={'class': 'togglewithip'}))
    ip_type = forms.ChoiceField(required=True, label=form_consts.IP.IP_TYPE)
    campaign = forms.ChoiceField(widget=forms.Select, required=False, label=form_consts.IP.CAMPAIGN)
    confidence = forms.ChoiceField(required=False, label=form_consts.IP.CAMPAIGN_CONFIDENCE)
    add_indicator = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'bulkskip'}), required=False, label=form_consts.IP.ADD_INDICATOR)
    indicator_reference = forms.CharField(widget=forms.TextInput(attrs={'size':'90', 'class':'bulkskip'}), required=False, label=form_consts.IP.INDICATOR_REFERENCE)
    related_id = forms.CharField(widget=forms.HiddenInput(), required=False, label=form_consts.Common.RELATED_ID)
    related_type = forms.CharField(widget=forms.HiddenInput(), required=False, label=form_consts.Common.RELATED_TYPE)
    relationship_type = forms.ChoiceField(required=False,
                                          label=form_consts.Common.RELATIONSHIP_TYPE,
                                          widget=forms.Select(attrs={'id':'relationship_type'}))

    def __init__(self, username, choices,  *args, **kwargs):
        super(AddIPForm, self).__init__(username, *args, **kwargs)

        if choices is None:
            self.fields['ip_type'].choices = ip_choices
        else:
            self.fields['ip_type'].choices = choices

        if username.has_access_to(Common.CAMPAIGN_READ):
            self.fields['campaign'].choices = [('', '')] + [
                (c.name, c.name) for c in get_item_names(Campaign, True)]
        self.fields['confidence'].choices = [('', ''),
                                             ('low', 'low'),
                                             ('medium', 'medium'),
                                             ('high', 'high')]

        self.fields['relationship_type'].choices = relationship_choices
        self.fields['relationship_type'].initial = RelationshipTypes.RELATED_TO

        add_bucketlist_to_form(self)
        add_ticket_to_form(self)

    def clean(self):
        cleaned_data = super(AddIPForm, self).clean()
        campaign = cleaned_data.get('campaign')

        if campaign:
            confidence = cleaned_data.get('confidence')

            if not confidence or confidence == '':
                self._errors.setdefault('confidence', ErrorList())
                self._errors['confidence'].append(u'This field is required if campaign is specified.')

        return cleaned_data
