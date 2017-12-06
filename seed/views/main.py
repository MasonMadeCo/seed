# !/usr/bin/env python
# encoding: utf-8
"""
:copyright (c) 2014 - 2017, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Department of Energy) and contributors. All rights reserved.  # NOQA
:author
"""

import json
import logging
import os
import pint
import subprocess
import xmltodict

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view

from seed import tasks
from seed.data_importer.models import ImportFile, ImportRecord
from seed.decorators import (
    ajax_request, get_prog_key
)
from seed.lib.mappings import mapper as simple_mapper
from seed.lib.mappings import mapping_data
from seed.lib.mcm import mapper
from seed.lib.superperms.orgs.decorators import has_perm
from seed.lib.superperms.orgs.models import OrganizationUser
from seed.models import (
    Column,
    get_column_mapping,
    PropertyState,
)
from seed.utils.api import api_endpoint
from seed.views.users import _get_js_role
from seed.pmintegration.manager import PortfolioManagerImport
from .. import search

_log = logging.getLogger(__name__)


def angular_js_tests(request):
    """Jasmine JS unit test code covering AngularJS unit tests"""
    return render(request, 'seed/jasmine_tests/AngularJSTests.html', locals())


def _get_default_org(user):
    """Gets the default org for a user and returns the id, name, and
    role_level. If no default organization is set for the user, the first
    organization the user has access to is set as default if it exists.

    :param user: the user to get the default org
    :returns: tuple (Organization id, Organization name, OrganizationUser role)
    """
    org = user.default_organization
    # check if user is still in the org, i.e. s/he wasn't removed from his/her
    # default org or did not have a set org and try to set the first one
    if not org or not user.orgs.exists():
        org = user.orgs.first()
        user.default_organization = org
        user.save()
    if org:
        org_id = org.pk
        org_name = org.name
        ou = user.organizationuser_set.filter(organization=org).first()
        # parent org owner has no role (None) yet has access to the sub-org
        org_user_role = _get_js_role(ou.role_level) if ou else ""
        return org_id, org_name, org_user_role
    else:
        return "", "", ""


@login_required
def home(request):
    """the main view for the app
        Sets in the context for the django template:

        * **app_urls**: a json object of all the URLs that is loaded in the JS global namespace
        * **username**: the request user's username (first and last name)
        * **AWS_UPLOAD_BUCKET_NAME**: S3 direct upload bucket
        * **AWS_CLIENT_ACCESS_KEY**: S3 direct upload client key
        * **FILE_UPLOAD_DESTINATION**: 'S3' or 'filesystem'
    """

    username = request.user.first_name + " " + request.user.last_name
    if 'S3' in settings.DEFAULT_FILE_STORAGE:
        FILE_UPLOAD_DESTINATION = 'S3'
        AWS_UPLOAD_BUCKET_NAME = settings.AWS_BUCKET_NAME
        AWS_CLIENT_ACCESS_KEY = settings.AWS_UPLOAD_CLIENT_KEY
    else:
        FILE_UPLOAD_DESTINATION = 'filesystem'

    initial_org_id, initial_org_name, initial_org_user_role = _get_default_org(
        request.user
    )

    return render(request, 'seed/index.html', locals())


@api_endpoint
@ajax_request
@api_view(['GET'])
def version(request):
    """
    Returns the SEED version and current git sha
    """
    manifest_path = os.path.dirname(
        os.path.realpath(__file__)) + '/../../package.json'
    with open(manifest_path) as package_json:
        manifest = json.load(package_json)

    sha = subprocess.check_output(
        ['git', 'rev-parse', '--short', 'HEAD']).strip()

    return JsonResponse({
        'version': manifest['version'],
        'sha': sha
    })


def error404(request):
    # Okay, this is a bit of a hack. Needed to move on.
    if '/api/' in request.path:
        return JsonResponse({
            "status": "error",
            "message": "Endpoint could not be found",
        }, status=status.HTTP_404_NOT_FOUND)
    else:
        response = render(request, 'seed/404.html', {})
        response.status_code = 404
        return response


def error500(request):
    # Okay, this is a bit of a hack. Needed to move on.
    if '/api/' in request.path:
        return JsonResponse({
            "status": "error",
            "message": "Internal server error",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        response = render(request, 'seed/500.html', {})
        response.status_code = 500
        return response


# @api_view(['POST'])  # do not add api_view on this because this is public and adding it will
# require authentication for some reason.
@ajax_request
def public_search(request):
    """the public API unauthenticated endpoint

    see ``search_buildings`` for the non-public version
    """
    orgs = search.get_orgs_w_public_fields()
    search_results, building_count = search.search_public_buildings(
        request, orgs
    )
    search_results = search.remove_results_below_q_threshold(search_results)
    search_results = search.paginate_results(request, search_results)
    search_results = search.mask_results(search_results)
    return JsonResponse({
        'status': 'success',
        'buildings': search_results,
        'number_matching_search': building_count,
        'number_returned': len(search_results)
    })


@api_endpoint
@ajax_request
@login_required
@api_view(['POST'])
def search_buildings(request):
    """
    Retrieves a paginated list of CanonicalBuildings matching search params.

    Payload::

        {
            'q': a string to search on (optional),
            'show_shared_buildings': True to include buildings from other orgs in this user's org tree,
            'order_by': which field to order by (e.g. pm_property_id),
            'import_file_id': ID of an import to limit search to,
            'filter_params': {
                a hash of Django-like filter parameters to limit query.  See seed.search.filter_other_params.
                If 'project__slug' is included and set to a project's slug, buildings will include associated labels
                for that project.
            }
            'page': Which page of results to retrieve (default: 1),
            'number_per_page': Number of buildings to retrieve per page (default: 10),
        }

    Returns::

        {
            'status': 'success',
            'buildings': [
                {
                    all fields for buildings the request user has access to, e.g.:
                        'canonical_building': the CanonicalBuilding ID of the building,
                        'pm_property_id': ID of building (from Portfolio Manager),
                        'address_line_1': First line of building's address,
                        'property_name': Building's name, if any
                    ...
                }...
            ]
            'number_matching_search': Total number of buildings matching search,
            'number_returned': Number of buildings returned for this page
        }
    """
    params = search.parse_body(request)

    orgs = request.user.orgs.select_related('parent_org').all()
    parent_org = orgs[0].parent_org

    buildings_queryset = search.orchestrate_search_filter_sort(
        params=params,
        user=request.user,
    )

    below_threshold = (
        parent_org and parent_org.query_threshold and
        len(buildings_queryset) < parent_org.query_threshold
    )

    buildings, building_count = search.generate_paginated_results(
        buildings_queryset,
        number_per_page=params['number_per_page'],
        page=params['page'],
        # Generally just orgs, sometimes all orgs with public fields.
        whitelist_orgs=orgs,
        below_threshold=below_threshold,
        matching=False
    )

    return JsonResponse({
        'status': 'success',
        'buildings': buildings,
        'number_matching_search': building_count,
        'number_returned': len(buildings)
    })


@ajax_request
@login_required
@api_view(['GET'])
def get_default_building_detail_columns(request):
    """Get default columns for building detail view.

    front end is expecting a JSON object with an array of field names

    Returns::

        {
            "columns": ["project_id", "name", "gross_floor_area"]
        }
    """
    columns = request.user.default_building_detail_custom_columns

    if columns == '{}' or isinstance(columns, dict):
        # Return empty result, telling the FE to show all.
        columns = []
    if isinstance(columns, unicode):
        # PostgreSQL 9.1 stores JSONField as unicode
        columns = json.loads(columns)

    return JsonResponse({
        'columns': columns,
    })


def _set_default_columns_by_request(body, user, field):
    """sets the default value for the user's default_custom_columns"""
    columns = body['columns']
    show_shared_buildings = body.get('show_shared_buildings')
    setattr(user, field, columns)
    if show_shared_buildings is not None:
        user.show_shared_buildings = show_shared_buildings
    user.save()
    return {}


@ajax_request
@login_required
@api_view(['POST'])
def set_default_columns(request):
    body = request.data
    return JsonResponse(
        _set_default_columns_by_request(body, request.user, 'default_custom_columns')
    )


@ajax_request
@login_required
@api_view(['POST'])
def set_default_building_detail_columns(request):
    body = request.data
    return JsonResponse(
        _set_default_columns_by_request(body, request.user,
                                        'default_building_detail_custom_columns')
    )


def _mapping_suggestions(import_file_id, org_id, user):
    """
    Temp function for allowing both api version for mapping suggestions to
    return the same data. Move this to the mapping_suggestions once we can
    deprecate the old get_column_mapping_suggestion method.

    :param import_file_id: import file id
    :param org_id: organization id of user
    :param user: user object from request
    :return: dict
    """
    result = {'status': 'success'}

    membership = OrganizationUser.objects.select_related('organization') \
        .get(organization_id=org_id, user=user)
    organization = membership.organization

    import_file = ImportFile.objects.get(
        pk=import_file_id,
        import_record__super_organization_id=organization.pk
    )

    # Get a list of the database fields in a list
    md = mapping_data.MappingData()

    # TODO: Move this to the MappingData class and remove calling add_extra_data
    # Check if there are any DB columns that are not defined in the
    # list of mapping data.
    # NL 12/2/2016: Removed 'organization__isnull' Query because we only want the
    # the ones belonging to the organization
    columns = list(Column.objects.select_related('unit').filter(
        mapped_mappings__super_organization_id=org_id).exclude(column_name__in=md.keys))
    md.add_extra_data(columns)

    # Portfolio manager files have their own mapping scheme - yuck, really?
    if import_file.from_portfolio_manager:
        _log.debug("map Portfolio Manager input file")
        suggested_mappings = simple_mapper.get_pm_mapping(import_file.first_row_columns,
                                                          resolve_duplicates=True)
    else:
        _log.debug("custom mapping of input file")
        # All other input types
        suggested_mappings = mapper.build_column_mapping(
            import_file.first_row_columns,
            md.keys_with_table_names,
            previous_mapping=get_column_mapping,
            map_args=[organization],
            thresh=80  # percentage match that we require. 80% is random value for now.
        )
        # replace None with empty string for column names and PropertyState for tables
        for m in suggested_mappings:
            table, field, conf = suggested_mappings[m]
            if field is None:
                suggested_mappings[m][1] = u''

    # Fix the table name, eventually move this to the build_column_mapping and build_pm_mapping
    for m in suggested_mappings:
        table, dest, conf = suggested_mappings[m]
        if not table:
            suggested_mappings[m][0] = 'PropertyState'

    result['suggested_column_mappings'] = suggested_mappings
    result['column_names'] = md.building_columns
    result['columns'] = md.data

    return result


@api_endpoint
@ajax_request
@login_required
@has_perm('requires_member')
@api_view(['DELETE'])
def delete_file(request):
    """
    Deletes an ImportFile from a dataset.

    Payload::

        {
            "file_id": "ImportFile id",
            "organization_id": "current user organization id as integer"
        }

    Returns::

        {
            'status': 'success' or 'error',
            'message': 'error message, if any'
        }
    """
    if request.method != 'DELETE':
        return JsonResponse({
            'status': 'error',
            'message': 'only HTTP DELETE allowed',
        })
    body = request.data
    file_id = body.get('file_id', '')
    import_file = ImportFile.objects.get(pk=file_id)
    d = ImportRecord.objects.filter(
        super_organization_id=body['organization_id'],
        pk=import_file.import_record.pk
    )
    # check if user has access to the dataset
    if not d.exists():
        return JsonResponse({
            'status': 'error',
            'message': 'user does not have permission to delete file',
        })

    # Note that the file itself is not delete, it remains on the disk/s3
    import_file.delete()
    return JsonResponse({'status': 'success'})


@api_endpoint
@ajax_request
@login_required
@permission_required('seed.can_access_admin')
@api_view(['DELETE'])
def delete_organization_inventory(request):
    """
    Starts a background task to delete all properties & taxlots
    in an org.

    :DELETE: Expects 'org_id' for the organization.

    Returns::

        {
            'status': 'success' or 'error',
            'progress_key': ID of background job, for retrieving job progress
        }
    """
    org_id = request.query_params.get('organization_id', None)
    deleting_cache_key = get_prog_key(
        'delete_organization_inventory',
        org_id
    )
    tasks.delete_organization_inventory.delay(org_id, deleting_cache_key)
    return JsonResponse({
        'status': 'success',
        'progress': 0,
        'progress_key': deleting_cache_key
    })


def pm_integration(request):
    return render(request, 'seed/pm_integration.html', {})


ATTRIBUTES_TO_PROCESS = [
    'national_median_site_energy_use',
    'site_energy_use',
    'source_energy_use',
    'site_eui',
    'source_eui'
]


def normalize_attribute(attribute_object):
    u_registry = pint.UnitRegistry()
    if '@uom' in attribute_object and '#text' in attribute_object:
        # this is the correct expected path for unit-based attributes
        string_value = attribute_object['#text']
        try:
            float_value = float(string_value)
        except ValueError:
            return {'status': 'error', 'message': 'Could not cast value to float: \"%s\"' % string_value}
        original_unit_string = attribute_object['@uom']
        if original_unit_string == u'kBtu':
            converted_value = float_value * 3.0
            return {'status': 'success', 'value': converted_value, 'units': str(u_registry.meter)}
        elif original_unit_string == u'kBtu/ft²':
            converted_value = float_value * 3.0
            return {'status': 'success', 'value': converted_value, 'units': str(u_registry.meter)}
        elif original_unit_string == u'Metric Tons CO2e':
            converted_value = float_value * 3.0
            return {'status': 'success', 'value': converted_value, 'units': str(u_registry.meter)}
        elif original_unit_string == u'kgCO2e/ft²':
            converted_value = float_value * 3.0
            return {'status': 'success', 'value': converted_value, 'units': str(u_registry.meter)}
        else:
            return {'status': 'error', 'message': 'Unsupported units string: \"%s\"' % original_unit_string}


@api_view(['POST'])
def pm_integration_get_templates(request):
    if 'email' not in request.data:
        return JsonResponse('Invalid call to PM worker: missing email for PM account')
    if 'username' not in request.data:
        return JsonResponse('Invalid call to PM worker: missing username for PM account')
    if 'password' not in request.data:
        return JsonResponse('Invalid call to PM worker: missing password for PM account')
    email = request.data['email']
    username = request.data['username']
    password = request.data['password']
    pm = PortfolioManagerImport(email, username, password)
    possible_templates = pm.get_list_of_report_templates()
    return JsonResponse({'status': 'success', 'templates': possible_templates})  # TODO: Could just return ['name']s...
    # print("  Index  |  Template Report Name  ")
    # print("---------|------------------------")
    # for i, t in enumerate(possible_templates):
    #     print("  %s  |  %s  " % (str(i).ljust(5), t['name']))
    # selection = raw_input("\nEnter an Index to download the report: ")
    # try:
    #     s_id = int(selection)
    # except ValueError:
    #     raise Exception("Invalid Selection; aborting.")
    # if 0 <= s_id < len(possible_templates):
    #     selected_template = possible_templates[s_id]
    # else:
    #     raise Exception("Invalid Selection; aborting.")


@api_view(['POST'])
def pm_integration_worker(request):
    if 'email' not in request.data:
        return JsonResponse('Invalid call to PM worker: missing email for PM account')
    if 'username' not in request.data:
        return JsonResponse('Invalid call to PM worker: missing username for PM account')
    if 'password' not in request.data:
        return JsonResponse('Invalid call to PM worker: missing password for PM account')
    if 'template_name' not in request.data:
        return JsonResponse('Invalid call to PM worker: missing template_name for PM account')
    email = request.data['email']
    username = request.data['username']
    password = request.data['password']
    template_name = request.data['template_name']
    pm = PortfolioManagerImport(email, username, password)
    possible_templates = pm.get_list_of_report_templates()
    selected_template = [p for p in possible_templates if p['name'] == template_name][0]  # TODO: Shouldn't need this
    content = pm.generate_and_download_template_report(selected_template)
    try:
        content_object = xmltodict.parse(content)
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'Malformed XML response from template download'}, status=500)
    success = True
    if 'report' not in content_object:
        success = False
    if 'informationAndMetrics' not in content_object['report']:
        success = False
    if 'row' not in content_object['report']['informationAndMetrics']:
        success = False
    if not success:
        return JsonResponse({'status': 'error',
                             'message': 'Template XML response was properly formatted but was missing expected keys.'},
                            status=500)
    properties = content_object['report']['informationAndMetrics']['row']

    # now we need to actually process each property
    # if we find a match we should update it, if we don't we should create it
    # then we should assign/update property values, possibly from this list?
    #  energy_score
    #  site_eui
    #  generation_date
    #  release_date
    #  source_eui_weather_normalized
    #  site_eui_weather_normalized
    #  source_eui
    #  energy_alerts
    #  space_alerts
    #  building_certification
    for prop in properties:
        seed_property_match = None

        # first try to match by pm property id if the PM report includes it
        if 'property_id' in prop:
            this_property_pm_id = prop['property_id']
            try:
                seed_property_match = PropertyState.objects.get(pm_property_id=this_property_pm_id)
                prop['MATCHED'] = 'Matched via pm_property_id'
            except PropertyState.DoesNotExist:
                seed_property_match = None

        # second try to match by address/city/state if the PM report includes it
        if not seed_property_match:
            if all(attr in prop for attr in ['address_1', 'city', 'state_province']):
                this_property_address_one = prop['address_1']
                this_property_city = prop['city']
                this_property_state = prop['state_province']
                try:
                    seed_property_match = PropertyState.objects.get(
                        address_line_1__iexact=this_property_address_one,
                        city__iexact=this_property_city,
                        state__iexact=this_property_state
                    )
                    prop['MATCHED'] = 'Matched via address/city/state'
                except PropertyState.DoesNotExist:
                    seed_property_match = None

        # if we didn't match then we need to create a new one
        if not seed_property_match:
            prop['MATCHED'] = 'NO! need to create new property'

        # either way at this point we should have a property, existing or new
        # so now we should process the attributes
        processed_attributes = {}
        for attribute_to_check in ATTRIBUTES_TO_PROCESS:
            if attribute_to_check in prop:
                found_attribute = prop[attribute_to_check]
                if isinstance(found_attribute, dict):
                    if found_attribute['#text']:
                        if found_attribute['#text'] == 'Not Available':
                            processed_attributes[attribute_to_check] = 'Requested variable blank/unavailable on PM'
                        else:
                            updated_attribute = normalize_attribute(found_attribute)
                            processed_attributes[attribute_to_check] = updated_attribute
                    else:
                        processed_attributes[attribute_to_check] = 'Malformed attribute did not have #text field'
                else:
                    pass  # nothing for now

        prop['PROCESSED'] = processed_attributes

    return JsonResponse({'status': 'success', 'properties': properties})
