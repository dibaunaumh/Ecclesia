from django.utils.translation import ugettext as _
from coa_workflow_manager import *

TEXT = "text"
HELP_LINK = "help_link"
POSITION = "position"
ICON = "icon"



# CoA workflow status hints
WORKFLOW_HINTS = {
    0: {
        TEXT: _("Please set your Goals: right-click the Goals column and choose 'Add story'"),
        HELP_LINK: "",
        POSITION: "goal",
        ICON: "",
    },

    ADD_GOALS: {
        TEXT: _("Please set your Goals: right-click the Goals column and choose 'Add story'"),
        HELP_LINK: "",
        POSITION: "goal",
        ICON: "",
    },

    ADD_CONDITIONS: {
        TEXT: _("Please add Conditions for reaching the Goals: right-click the Conditions column and choose 'Add story'"),
        HELP_LINK: "",
        POSITION: "condition",
        ICON: "",
    },

    ADD_RELATIONS_FROM_CONDITIONS_TO_GOALS: {
        TEXT: _("Please add relations from Conditions to Goals: right-click the Conditions and choose 'Add relation'"),
        HELP_LINK: "",
        POSITION: "condition",
        ICON: "",
    },

    ADD_OPTIONS: {
        TEXT: _("Please set Options for reaching the Goals: right-click the Options column and choose 'Add story'"),
        HELP_LINK: "",
        POSITION: "option",
        ICON: "",
    },

    ADD_EFFECTS: {
        TEXT: _("Please describe the Effects of each Option: right-click the Effects column and choose 'Add story'"),
        HELP_LINK: "",
        POSITION: "effect",
        ICON: "",
    },

    ADD_RELATIONS_FROM_OPTIONS_TO_EFFECTS: {
        TEXT: _("Please add relations from Options to Effects: right-click the Options and choose 'Add relation'"),
        HELP_LINK: "",
        POSITION: "option",
        ICON: "",
    },

    ADD_OPINIONS_ON_STORIES: {
        TEXT: _("Please describe your opinion on each story: Right-click a story and choose 'Add opinion'"),
        HELP_LINK: "",
        POSITION: "top",
        ICON: "",
    },

    ADD_OPINIONS_ON_RELATIONS: {
        TEXT: _("Please describe your opinion on each relation: Right-click a relation and choose 'Add opinion'"),
        HELP_LINK: "",
        POSITION: "top",
        ICON: "",
    },

    START_VOTE: {
        TEXT: _("You can now start a Voting session: Click the 'Start vote' button"),
        HELP_LINK: "",
        POSITION: "vote",
        ICON: "",
    },
    
}