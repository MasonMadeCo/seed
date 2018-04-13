# !/usr/bin/env python
# encoding: utf-8
"""
:copyright (c) 2014 - 2018, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Department of Energy) and contributors. All rights reserved.  # NOQA
:author
"""
from datetime import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone

from seed.landing.models import SEEDUser as User
from seed.lib.superperms.orgs.models import Organization, OrganizationUser
from seed.models import (
    PropertyView,
    StatusLabel,
)
from seed.test_helpers.fake import (
    FakeCycleFactory, FakeColumnFactory,
    FakePropertyFactory, FakePropertyStateFactory,
    FakeTaxLotStateFactory
)
from seed.tests.util import DeleteModelsTestCase


class InventoryViewTests(DeleteModelsTestCase):
    def setUp(self):
        user_details = {
            'username': 'test_user@demo.com',
            'password': 'test_pass',
            'email': 'test_user@demo.com'
        }
        self.user = User.objects.create_superuser(**user_details)
        self.org = Organization.objects.create()
        self.column_factory = FakeColumnFactory(organization=self.org)
        self.cycle_factory = FakeCycleFactory(organization=self.org,
                                              user=self.user)
        self.property_factory = FakePropertyFactory(organization=self.org)
        self.property_state_factory = FakePropertyStateFactory(organization=self.org)
        self.taxlot_state_factory = FakeTaxLotStateFactory(organization=self.org)
        self.org_user = OrganizationUser.objects.create(
            user=self.user, organization=self.org
        )
        self.cycle = self.cycle_factory.get_cycle(
            start=datetime(2010, 10, 10, tzinfo=timezone.get_current_timezone()))
        self.status_label = StatusLabel.objects.create(
            name='test', super_organization=self.org
        )
        self.client.login(**user_details)

    def test_get_building_sync(self):
        state = self.property_state_factory.get_property_state()
        prprty = self.property_factory.get_property()
        pv = PropertyView.objects.create(
            property=prprty, cycle=self.cycle, state=state
        )

        # go to buildingsync endpoint
        params = {
            'organization_id': self.org.pk
        }
        url = reverse('api:v2.1:properties-building-sync', args=[pv.id])
        response = self.client.get(url, params)
        self.assertIn('<auc:FloorAreaValue>%s.0</auc:FloorAreaValue>' % state.gross_floor_area, response.content)

    def test_get_hpxml(self):
        state = self.property_state_factory.get_property_state()
        prprty = self.property_factory.get_property()
        pv = PropertyView.objects.create(
            property=prprty, cycle=self.cycle, state=state
        )

        # go to buildingsync endpoint
        params = {
            'organization_id': self.org.pk
        }
        url = reverse('api:v2.1:properties-hpxml', args=[pv.id])
        response = self.client.get(url, params)
        self.assertIn('<GrossFloorArea>%s.0</GrossFloorArea>' % state.gross_floor_area, response.content)
