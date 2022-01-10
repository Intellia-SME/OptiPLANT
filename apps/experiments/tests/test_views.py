from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import FieldFile
from django.test import TestCase
from django.urls import resolve
from django.utils import timezone

from apps.core.constants import MAX_DATASET_SIZE

from ..forms import CreateExperimentForm
from ..models import Experiment
from ..views import CreateExperimentView

UserModel = get_user_model()


class CreateExperimentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(username='guest', email="guest@guest.gr")
        cls.url = '/experiments/create/'

    def setUp(self):
        self.client.force_login(self.user)

    def tearDown(self):
        """
        To delete all dummy csv files from disk
        """
        for experiment in Experiment.objects.all():
            experiment.delete()
        super().tearDown()

    def test_expriment_url_resolves_to_CreateExperimentView(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, CreateExperimentView.as_view().__name__)

    def test_methods_allowed(self):
        response = self.client.options(self.url)
        self.assertEqual(response['allow'], 'GET, POST')

    def test_GET_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'experiments/create_experiment.html')

    def test_GET_has_CreateExperimentForm(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], CreateExperimentForm)

    def test_unauthorized_user_redirect(self):
        self.client.logout()
        response = self.client.options(self.url)
        self.assertEqual(response.status_code, 302)

    def test_unauthorized_user_redirect_page(self):
        self.client.logout()
        response = self.client.options(self.url)
        self.assertRedirects(response, '/accounts/login/?next=/experiments/create/')

    def test_POST_success_creates_new_experiment(self):
        self.client.post(
            self.url,
            data={
                "name": "test_demo",
                "dataset": SimpleUploadedFile("demo_file.csv", b"Dummy"),
            },
        )
        self.assertEqual(Experiment.objects.count(), 1)
        self.assertEqual(Experiment.objects.first().name, "test_demo")

    def test_POST_success_creates_saves_dataset(self):
        self.client.post(
            self.url,
            data={
                "name": "test_demo",
                "dataset": SimpleUploadedFile("demo_file.csv", b"Dummy"),
            },
        )
        self.assertEqual(
            Experiment.objects.first().dataset.url,
            f"/datasets/{self.user.username}/{timezone.now().date().strftime('%Y/%m')}/"
            f"{Experiment.objects.first().id}.csv",
        )

    def test_POST_success_redirects_to_homepage(self):
        response = self.client.post(
            self.url,
            data={
                "name": "test_demo",
                "dataset": SimpleUploadedFile("demo_file.csv", b"Dummy"),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        self.assertEqual(response['location'], '/')

    def test_POST_success_saves_description(self):
        self.client.post(
            self.url,
            data={
                "name": "test_demo",
                "description": "Dummy",
                "dataset": SimpleUploadedFile("demo_file.csv", b"Dummy"),
            },
        )
        self.assertEqual(Experiment.objects.first().description, "Dummy")

    def test_POST_success_saves_experiment_to_correct_user(self):
        another_user = UserModel.objects.create_user(username='guest2', email="guest2@guest.gr")
        self.client.post(
            self.url,
            data={
                "name": "test_demo",
                "description": "Dummy",
                "dataset": SimpleUploadedFile("demo_file.csv", b"Dummy"),
            },
        )
        self.assertEqual(Experiment.objects.filter(experimenter=self.user).count(), 1)
        self.assertEqual(Experiment.objects.filter(experimenter=another_user).count(), 0)

    def test_POST_validation_error_required_fields(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Experiment.objects.count(), 0)
        self.assertTrue('required' in response.context['form'].errors['name'][0])
        self.assertTrue('required' in response.context['form'].errors['dataset'][0])

    def test_POST_validation_error_file_extension(self):
        response = self.client.post(
            self.url,
            data={
                "name": "test_demo",
                "description": "Dummy",
                "dataset": SimpleUploadedFile("demo_file.txt", b"Dummy"),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Experiment.objects.count(), 0)
        self.assertTrue('File extension “txt” is not allowed.' in response.context['form'].errors['dataset'][0])

    def test_POST_validation_error_big_file(self):
        with patch.object(FieldFile, 'size', MAX_DATASET_SIZE + 1):
            response = self.client.post(
                self.url,
                data={
                    "name": "test_demo",
                    "description": "Dummy",
                    "dataset": SimpleUploadedFile("demo_file.csv", b"Dummy"),
                },
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Experiment.objects.count(), 0)
            self.assertTrue('demo_file.csv must be less than 1MB' in response.context['form'].errors['dataset'][0])
