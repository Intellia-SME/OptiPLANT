from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.core.constants import MAX_DATASET_SIZE

from ..validators import validate_size


class ExperimentValidatorTest(TestCase):
    def test_validation_error_with_big_file_more_than_1MB(self):
        big_file = SimpleUploadedFile("demo_file.csv", b"Dummy")
        big_file.size = MAX_DATASET_SIZE + 1
        with self.assertRaises(ValidationError) as e:
            validate_size(big_file)
        self.assertEqual(e.exception.messages[0], 'demo_file.csv must be less than 1MB')

    def test_no_validation_error_with_file_less_than_1MB(self):
        big_file = SimpleUploadedFile("demo_file.csv", b"Dummy")
        big_file.size = MAX_DATASET_SIZE
        try:
            validate_size(big_file)
        except ValidationError:
            self.fail("big_file() raised ValidationError unexpectedly!")
