from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import resolve

from ..json_views import JSONExperimentStatisticsView
from ..models import Experiment

UserModel = get_user_model()


class JSONExperimentStatisticsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(username='guest', email="guest@guest.gr")
        cls.experiment = Experiment.objects.create(
            experimenter=cls.user, name="test_demo", dataset=SimpleUploadedFile("demo_file.csv", b"Dummy")
        )
        cls.url = f"/experiments/{cls.experiment.id}/main/get-statistics/"

    def setUp(self):
        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        cls.experiment.delete()
        super().tearDownClass()

    def test_url_resolves_to_JSONExperimentStatisticsViewTest(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, JSONExperimentStatisticsView.as_view().__name__)

    def test_methods_allowed(self):
        response = self.client.options(self.url)
        self.assertEqual(response['allow'], 'GET')

    def test_unauthorized_user_redirect(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_only_the_experiments_owner_can_see_the_his_statistics(self):
        self.client.logout()
        another_user = UserModel.objects.create_user(username='guest2', email="guest2@guest.gr")
        self.client.force_login(another_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
