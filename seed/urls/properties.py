# !/usr/bin/env python
# encoding: utf-8
"""
:copyright (c) 2014 - 2016, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Department of Energy) and contributors. All rights reserved.  # NOQA
:author
"""

from django.conf.urls import url

from seed.views.properties import (get_properties, get_property_columns,
                                   get_taxlots, get_taxlot_columns,
                                   get_cycles, Property, TaxLot)

from seed.views.reports import Report

urlpatterns = [
    url(r'^properties/$', get_properties, name='properties'),
    url(r'^taxlots/$', get_taxlots, name='taxlots'),
    url(r'^cycles/$', get_cycles, name='cycles'),
    url(r'^property-columns/$', get_property_columns, name='property-columns'),
    url(r'^taxlot-columns/$', get_taxlot_columns, name='taxlot-columns'),
    url(r'^properties/(?P<property_pk>\d+)/cycles/(?P<cycle_pk>\d+)/$',
        Property.as_view({'get': 'get_property'}), name='property-details'),
    url(r'^update-properties/(?P<property_pk>\d+)/cycles/(?P<cycle_pk>\d+)/$',
        Property.as_view({'put': 'put'}), name='update-property-details'),
    url(r'^taxlots/(?P<taxlot_pk>\d+)/cycles/(?P<cycle_pk>\d+)/$',
        TaxLot.as_view({'get': 'get_taxlot'}), name='taxlot-details'),
    url(r'^update-taxlots/(?P<taxlots_pk>\d+)/cycles/(?P<cycle_pk>\d+)/$',
        TaxLot.as_view({'put': 'put'}), name='update-taxlot-details'),
    url(r'^get_property_report_data/$',
        Report.as_view({'get': 'get_property_report_data'}),
        name='property_report_data'),
    url(r'^get_aggregated_property_report_data/$',
        Report.as_view({'get': 'get_aggregated_property_report_data'}),
        name='aggregated_property_report_data'),
]