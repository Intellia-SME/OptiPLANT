from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase

from apps.core.constants import MAX_DATASET_SIZE

from ..forms import CreateExperimentForm
from ..models import Experiment

UserModel = get_user_model()


class CreateExperimentFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        To test CreateExperimentForm, you need to pass a request (with a user) to the form,
        before calling the is_valid or save form's methods.
        A dummy request (using RequestFactory) is created for that reason.
        """
        cls.user = UserModel.objects.create_user(username='guest', email="guest@guest.gr")
        cls.request = RequestFactory()
        cls.request.user = cls.user

    def tearDown(self):
        """
        To delete all dummy csv files from disk
        """
        for experiment in Experiment.objects.all():
            experiment.delete()
        super().tearDown()

    def test_valid_form_creates_experiment(self):
        form = CreateExperimentForm({"name": "test_demo"}, {"dataset": SimpleUploadedFile("demo_file.csv", b"Dummy")})
        form.request = self.request
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Experiment.objects.count(), 1)

    def test_valid_form_with_desciption(self):
        form = CreateExperimentForm(
            {"name": "test_demo", "description": "Dummy"},
            {"dataset": SimpleUploadedFile("demo_file.csv", b"Dummy")},
        )
        form.request = self.request
        form.save()
        self.assertEqual(Experiment.objects.first().description, "Dummy")

    def test_form_creates_an_experiment_that_belongs_to_the_user_of_the_request(self):
        another_user = UserModel.objects.create_user(username='guest2', email="guest2@guest.gr")
        form = CreateExperimentForm({"name": "test_demo"}, {"dataset": SimpleUploadedFile("demo_file.csv", b"Dummy")})
        form.request = self.request
        form.save()
        self.assertEqual(Experiment.objects.filter(experimenter=self.user).count(), 1)
        self.assertEqual(Experiment.objects.filter(experimenter=another_user).count(), 0)

    def test_invalid_form_required_fields_name_dataset(self):
        form = CreateExperimentForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"][0], "This field is required.")
        self.assertEqual(form.errors["dataset"][0], "This field is required.")

    def test_invalid_form_file_extension(self):
        form = CreateExperimentForm({"name": "test_demo"}, {"dataset": SimpleUploadedFile("demo_file.txt", b"Dummy")})
        form.request = self.request
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["dataset"][0], "File extension “txt” is not allowed. Allowed extensions are: csv."
        )

    def test_invalid_form_big_file(self):
        big_file = SimpleUploadedFile("demo_file.csv", b"Dummy")
        big_file.size = MAX_DATASET_SIZE + 1
        form = CreateExperimentForm({"name": "test_demo"}, {"dataset": big_file})
        form.request = self.request
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["dataset"][0], "demo_file.csv must be less than 1MB")
