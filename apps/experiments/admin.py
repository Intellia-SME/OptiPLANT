from django.contrib import admin
from django.utils.html import format_html

from .models import Experiment


class ExperimentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "experimenter", "dataset_link", "created_at"]
    search_fields = [
        "name",
    ]
    list_filter = [
        "experimenter",
    ]
    readonly_fields = [
        "modified_at",
        "created_at",
    ]
    date_hierarchy = 'created_at'

    def dataset_link(self, obj):
        return format_html('<a href="{0}">Download</a>'.format(obj.dataset.url))

    dataset_link.short_description = 'Dataset'
    dataset_link.allow_tags = True


admin.site.register(Experiment, ExperimentAdmin)
