from django.http import HttpResponseForbidden


class ObjectOwnershipRequiredMixin:
    """Verify that the current user is the object's owner."""

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().experimenter != self.request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
