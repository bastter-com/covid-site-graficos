from .base_testcase import BaseTestCaseWorldTotalData
from world.models import WorldTotalData
from world.services import save_total_world_data


class WorldTotalDataTestSuite(BaseTestCaseWorldTotalData):
    def setUp(self):
        super().setUp()

    def test_if_data_is_in_database(self):
        queryset = WorldTotalData.objects.all()
        self.assertTrue(queryset)

    def test_if_database_has_30_registered_rows(self):
        queryset = WorldTotalData.objects.all()
        self.assertEqual(len(queryset), 30)

    # def test_date_list_creation_function(self):
    #     date_list = save_total_world_data.create_date_list()
    #     self.assertTrue(date_list)
