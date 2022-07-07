# Generated by Django 3.2.12 on 2022-06-29 14:29
# this is identical to migration 0163 but BAE was updated so need to change (to include bae v0.1.9)

from django.db import migrations

from seed.lib.xml_mapping.mapper import get_bae_mappings


def update_bae_fields(apps, schema_editor):
    """create a default BuildingSync column mapping preset for each organization"""
    Organization = apps.get_model("orgs", "Organization")

    # profile number for 'BuildingSync Default' profile is 1
    prof_type = 1

    # 'Audit Template Building Id' name matches the automatically generated field name from
    # the default_buildingsync_profile_mappings method.
    # this should already be taken care of by 169
    # new_mappings = [
    #     {
    #         'from_field': '/auc:BuildingSync/auc:Facilities/auc:Facility/auc:Sites/auc:Site/auc:Buildings/auc:Building/auc:PremisesIdentifiers/auc:PremisesIdentifier[auc:IdentifierCustomName="Audit Template Building ID"]/auc:IdentifierValue',
    #         'from_field_value': 'text',
    #         'from_units': None,
    #         'to_table_name': 'PropertyState',
    #         'to_field': 'Audit Template Building Id', 
    #     },
    #     {
    #         'from_field': '/auc:BuildingSync/auc:Facilities/auc:Facility/auc:Sites/auc:Site/auc:Buildings/auc:Building/auc:PremisesIdentifiers/auc:PremisesIdentifier[auc:IdentifierCustomName="Portfolio Manager Building ID"]/auc:IdentifierValue',
    #         'from_field_value': 'text',
    #         'from_units': None,
    #         'to_table_name': 'PropertyState',
    #         'to_field': 'pm_property_id',
    #     }
    # ]

    # get BAE fields
    new_mappings = get_bae_mappings()
    print(f"MAPPINGS: {new_mappings}")

    for org in Organization.objects.all():
        # first find current BuildingSync mapping
        profiles = org.columnmappingprofile_set.filter(profile_type=prof_type)

        for prof in profiles:
            for new_mapping in new_mappings:

                # verify that the new mapping does not already exist, only check the to_table_name
                # and to_field. We don't want to create two mappings to the same table/field.
                map_exist_check = [{'f': m['to_field'], 't': m['to_table_name']} for m in prof.mappings]
                if {'f': new_mapping['to_field'], 't': new_mapping['to_table_name']} in map_exist_check:
                    print(f"BuildingSync mapping already exists for {new_mapping['to_field']}, skipping")
                    continue
                else:
                    # add the mapping since it doesn't already exist
                    prof.mappings.append(new_mapping)

            prof.save()


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0170_column_derived_column'),
    ]

    operations = [
        migrations.RunPython(update_bae_fields)
    ]
