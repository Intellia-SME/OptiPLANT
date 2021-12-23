from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase
from django.views.generic.base import TemplateView

from ..mixins import ObjectOwnershipRequiredMixin
from ..models import Experiment

UserModel = get_user_model()


class DummyView(ObjectOwnershipRequiredMixin, TemplateView):
    template_name = 'dummy.html'

    def get_object(self):
        return Experiment.objects.first()


class ObjectOwnershipRequiredMixinTest(TestCase):
    factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(username='guest', email="guest@guest.gr")
        cls.another_user = UserModel.objects.create_user(username='guest2', email="guest2@guest.gr")
        cls.experiment = Experiment.objects.create(
            experimenter=cls.user, name="test_demo", dataset=SimpleUploadedFile("demo_file.csv", b"Dummy")
        )

    @classmethod
    def tearDownClass(cls):
        cls.experiment.delete()
        super().tearDownClass()

    def test_forbidden_access_for_no_owner(self):
        view = DummyView.as_view()
        request = self.factory.get('/rand')
        request.user = self.another_user
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_owner_has_access(self):
        view = DummyView.as_view()
        request = self.factory.get('/rand')
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
