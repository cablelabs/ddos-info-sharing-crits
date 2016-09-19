from mongoengine import Document, StringField, IntField, FloatField
from django.conf import settings

from crits.vocabulary.ips import IPTypes

from crits.core.crits_mongoengine import CritsBaseAttributes, CritsSourceDocument, CritsActionsDocument
from crits.ips.migrate import migrate_ip


class IP(CritsBaseAttributes, CritsActionsDocument, CritsSourceDocument, Document):
    """
    IP class.
    """

    meta = {
        "collection": settings.COL_IPS,
        "crits_type": 'IP',
        "latest_schema_version": 3,
        "schema_doc": {
            'ip': 'The IP address',
            'type': ('The type of IP address.'
                    ' Object Types'),
        },
        "jtable_opts": {
                         'details_url': 'crits.ips.views.ip_detail',
                         'details_url_key': 'ip',
                         'default_sort': "modified DESC",
                         'searchurl': 'crits.ips.views.ips_listing',
                         'fields': [ "ip", "ip_type", "created", "modified",
                                     "source", "campaign", "status", "id"],
                         'jtopts_fields': [ "details",
                                            "ip",
                                            "type",
                                            "created",
                                            "modified",
                                            "source",
                                            "campaign",
                                            "status",
                                            "favorite",
                                            "id"],
                         'hidden_fields': [],
                         'linked_fields': ["ip", "source", "campaign", "type"],
                         'details_link': 'details',
                         'no_sort': ['details']
                       }

    }

    ip = StringField(required=True)
    ip_type = StringField(default=IPTypes.IPV4_ADDRESS, db_field="type")
    misc = StringField(default='')

    # New fields
    alert_type = StringField(default='')
    asn = StringField(default='')
    city = StringField(default='')
    country = StringField(default='')
    first_seen = StringField(default='')
    last_seen = StringField(default='')
    number_of_times = IntField()
    state = StringField(default='')
    total_bps = IntField()
    total_pps = IntField()
    attack_type = StringField(default='')
    vendor = StringField(default='')

    def migrate(self):
        migrate_ip(self)

    def edit_misc(self, misc):
        """
        Change the IP misc field.

        :param misc: The new misc string.
        :type misc: str

        """

        self.misc = misc
