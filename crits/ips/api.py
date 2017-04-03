from django.core.urlresolvers import reverse
from tastypie import authorization
from tastypie.authentication import MultiAuthentication

from crits.ips.ip import IP
from crits.ips.handlers import ip_add_update
from crits.core.api import CRITsApiKeyAuthentication, CRITsSessionAuthentication
from crits.core.api import CRITsSerializer, CRITsAPIResource


class IPResource(CRITsAPIResource):
    """
    Class to handle everything related to the IP API.

    Currently supports GET and POST.
    """

    class Meta:
        object_class = IP
        allowed_methods = ('get', 'post', 'patch')
        resource_name = "ips"
        authentication = MultiAuthentication(CRITsApiKeyAuthentication(),
                                             CRITsSessionAuthentication())
        authorization = authorization.Authorization()
        serializer = CRITsSerializer()

    def get_object_list(self, request):
        """
        Use the CRITsAPIResource to get our objects but provide the class to get
        the objects from.

        :param request: The incoming request.
        :type request: :class:`django.http.HttpRequest`
        :returns: Resulting objects in the specified format (JSON by default).

        """

        return super(IPResource, self).get_object_list(request, IP)

    def obj_create(self, bundle, **kwargs):
        """
        Handles creating IPs through the API.

        :param bundle: Bundle containing the information to create the IP.
        :type bundle: Tastypie Bundle object.
        :returns: HttpResponse.
        """

        analyst = bundle.request.user.username
        data = bundle.data
        ip = data.get('ip', None)
        name = data.get('source', None)
        reference = data.get('reference', None)
        method = data.get('method', None)
        campaign = data.get('campaign', None)
        description = data.get('description', None)
        confidence = data.get('confidence', None)
        ip_type = data.get('ip_type', None)
        add_indicator = data.get('add_indicator', False)
        indicator_reference = data.get('indicator_reference', None)
        bucket_list = data.get('bucket_list', None)
        ticket = data.get('ticket', None)

        # New fields
        # extra = data.get('extra', None)
        # as_number = data.get('as_number', None)
        # attack_type = data.get('attack_type', None)
        # city = data.get('city', None)
        # country = data.get('country', None)
        # first_seen = data.get('first_seen', None)
        # last_seen = data.get('last_seen', None)
        # number_of_times = data.get('number_of_times', None)
        # state = data.get('state', None)
        # total_bps = data.get('total_bps', None)
        # total_pps = data.get('total_pps', None)

        content = {'return_code': 1,
                   'type': 'IP'}

        if not ip or not name or not ip_type:
            content['message'] = "Must provide an IP, IP Type, and Source."
            self.crits_response(content)

        result = ip_add_update(ip,
                               ip_type,
                               source=name,
                               source_method=method,
                               source_reference=reference,
                               campaign=campaign,
                               confidence=confidence,
                               description=description,
                               analyst=analyst,
                               bucket_list=bucket_list,
                               ticket=ticket,
                               is_add_indicator=add_indicator,
                               indicator_reference=indicator_reference,
                               # extra=extra,
                               # as_number=as_number,
                               # attack_type=attack_type,
                               # city=city,
                               # country=country,
                               # first_seen=first_seen,
                               # last_seen=last_seen,
                               # number_of_times=number_of_times,
                               # state=state,
                               # total_bps=total_bps,
                               # total_pps=total_pps
                               )

        if result.get('message'):
            content['message'] = result.get('message')
        if result.get('object'):
            content['id'] = str(result.get('object').id)
        if content.get('id'):
            url = reverse('api_dispatch_detail',
                          kwargs={'resource_name': 'ips',
                                  'api_name': 'v1',
                                  'pk': content.get('id')})
            content['url'] = url
        if result['success']:
            content['return_code'] = 0
        self.crits_response(content)
