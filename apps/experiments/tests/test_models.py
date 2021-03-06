from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import FieldFile
from django.test import TestCase
from django.utils import timezone

from apps.core.constants import MAX_DATASET_SIZE, MAX_TRAINING_COST

from ..models import Experiment

UserModel = get_user_model()


class ExperimentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(username='guest', email="guest@guest.gr")
        cls.experiment = Experiment.objects.create(
            experimenter=cls.user, name="test_demo", dataset=SimpleUploadedFile("demo_file.csv", b"Dummy")
        )

    @classmethod
    def tearDownClass(cls):
        cls.experiment.delete()
        super().tearDownClass()

    def test_experiment_inserted(self):
        self.assertEqual(Experiment.objects.count(), 1)

    def test_experiment_correct_name(self):
        self.assertEqual(Experiment.objects.first().name, "test_demo")

    def test_experiment_str(self):
        self.assertEqual(Experiment.objects.first().__str__(), "test_demo")

    def test_experiment_can_update_description(self):
        self.experiment.description = "Dummy"
        self.experiment.save()
        self.assertEqual(Experiment.objects.first().description, "Dummy")

    def test_experiment_dataset_url(self):
        self.assertEqual(
            Experiment.objects.first().dataset.url,
            f"/datasets/{self.user.username}/{timezone.now().date().strftime('%Y/%m')}/{self.experiment.id}.csv",
        )

    def test_experiment_cost_is_correctly_calculated_for_small_dataset(self):
        self.assertGreater(MAX_DATASET_SIZE, Experiment.objects.first().dataset.size)
        self.assertEqual(Experiment.objects.first().training_cost, MAX_TRAINING_COST / 2)

    def test_experiment_cost_is_correctly_calculated_for_big_dataset(self):
        with patch.object(FieldFile, 'size', MAX_DATASET_SIZE):
            self.assertEqual(MAX_DATASET_SIZE, Experiment.objects.first().dataset.size)
            self.assertEqual(Experiment.objects.first().training_cost, MAX_TRAINING_COST)

    def test_experiment_required_fields(self):
        with self.assertRaises(ValidationError) as e:
            Experiment.objects.create()
        self.assertEqual(e.exception.message_dict['name'][0], "This field cannot be blank.")
        self.assertEqual(e.exception.message_dict['experimenter'][0], "This field cannot be null.")
        self.assertEqual(e.exception.message_dict['dataset'][0], "This field cannot be blank.")

    def test_experiment_validation_error_dataset_bigger_than_1MB(self):
        big_file = SimpleUploadedFile("demo_file.csv", b"Dummy")
        big_file.size = MAX_DATASET_SIZE + 1
        with self.assertRaises(ValidationError) as e:
            self.experiment.dataset = big_file
            self.experiment.save()
        self.assertEqual(e.exception.messages[0], 'demo_file.csv must be less than 1MB')

    def test_experiment_validation_error_dataset_not_a_csv(self):
        with self.assertRaises(ValidationError) as e:
            self.experiment.dataset = SimpleUploadedFile("demo_file.txt", b"Dummy")
            self.experiment.save()
        self.assertEqual(e.exception.messages[0], 'File extension ???txt??? is not allowed. Allowed extensions are: csv.')
