from coa_workflow_manager import *
from django.utils.translation import ugettext as _

# hint metadata fields
import coa_workflow_hints
from django.template.loader import render_to_string


def get_workflow_hints(discussion):
    if discussion.type.name == "course-of-action":
        metadata = coa_workflow_hints.WORKFLOW_HINTS
        for key, md in metadata.items():
            md["hint_html"] = render_to_string("hint.html", md)
        return metadata

    return None