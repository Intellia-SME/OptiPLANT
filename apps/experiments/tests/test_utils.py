from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from ..models import Experiment
from ..utils import file_directory_path

UserModel = get_user_model()


class ExperimentUtilsTest(TestCase):
    def test_file_directory_path(self):
        user = UserModel(username="guest")
        experiment = Experiment(experimenter=user)
        self.assertEqual(
            file_directory_path(experiment, "demo_file.csv"),
            f"datasets/{user.username}/{timezone.now().date().strftime('%Y/%m')}/{experiment.id}.csv",
        )
