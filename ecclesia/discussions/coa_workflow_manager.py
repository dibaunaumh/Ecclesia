from django.db.models import get_model


# CoA workflow status
INITIAL = 0
ADD_GOALS = 1
ADD_CONDITIONS = 2
ADD_RELATIONS_FROM_CONDITIONS_TO_GOALS = 3
ADD_OPTIONS = 4
ADD_EFFECTS = 5
ADD_RELATIONS_FROM_OPTIONS_TO_EFFECTS = 6
ADD_OPINIONS_ON_STORIES = 7
ADD_OPINIONS_ON_RELATIONS = 8
START_VOTE = 9
DONE = 10

DEFAULT_STATUS = ADD_GOALS


def update_workflow_status(discussion):
    """
    Check the current status & accordingly the conditions
    that change the status to a different status.
    """
    current_status = discussion.workflow_status
    if current_status == INITIAL:
            current_status = ADD_GOALS
    new_status = {
        ADD_GOALS:
            lambda discussion: ADD_CONDITIONS if check_stories_of_type(discussion, "goal") else ADD_GOALS,

        ADD_CONDITIONS:
            lambda discussion: ADD_RELATIONS_FROM_CONDITIONS_TO_GOALS if check_stories_of_type(discussion, "goal_condition") else ADD_CONDITIONS,

        ADD_RELATIONS_FROM_CONDITIONS_TO_GOALS:
            lambda discussion: ADD_OPTIONS if check_stories_of_type(discussion, "relation") else ADD_RELATIONS_FROM_CONDITIONS_TO_GOALS,

        ADD_OPTIONS:
            lambda discussion: ADD_EFFECTS if check_stories_of_type(discussion, "goal") else ADD_OPTIONS,

        ADD_EFFECTS:
            lambda discussion: ADD_RELATIONS_FROM_OPTIONS_TO_EFFECTS if check_stories_of_type(discussion, "goal") else ADD_EFFECTS,

        ADD_RELATIONS_FROM_OPTIONS_TO_EFFECTS:
            lambda discussion: ADD_OPINIONS_ON_STORIES if check_stories_of_type(discussion, "goal") else ADD_RELATIONS_FROM_OPTIONS_TO_EFFECTS,

        ADD_OPINIONS_ON_STORIES:
            lambda discussion: ADD_OPINIONS_ON_RELATIONS if check_stories_of_type(discussion, "goal") else ADD_OPINIONS_ON_STORIES,

        ADD_OPINIONS_ON_RELATIONS:
            lambda discussion: START_VOTE if check_stories_of_type(discussion, "goal") else ADD_OPINIONS_ON_RELATIONS,

        START_VOTE:
            lambda discussion: DONE if check_voting(discussion) else START_VOTE,

        DONE:
            lambda discussion : DONE,
    }[current_status](discussion)
    if new_status != current_status:
        discussion.workflow_status = new_status
        discussion.save()
    
    
def check_stories_of_type(discussion, speech_act):
    SpeechAct = get_model("discussions", "SpeechAct")
    speech_act_obj = SpeechAct.objects.get(name=speech_act)
    model = get_model("discussions", "BaseStory")
    return model.objects.filter(discussion=discussion, speech_act=speech_act_obj).count()



def check_voting(discussion):
    Voting = get_model("voting", "Voting")
    return Voting.objects.filter(discussion=discussion).count()


