from django.db.models import get_model


# CoA workflow status
NOT_ALLOWED_TO_EDIT = -1
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

    conditions = [
            lambda discussion: True,
            lambda discussion: check_stories_of_type(discussion, "goal"),
            lambda discussion: check_stories_of_type(discussion, "condition"),
            lambda discussion: check_stories_of_type(discussion, "relation"),
            lambda discussion: True, #check_stories_of_type(discussion, "opinion"),
            lambda discussion: check_stories_of_type(discussion, "effect"),
            lambda discussion: True, #check_stories_of_type(discussion, "relation"),
            lambda discussion: True, #check_stories_of_type(discussion, "opinion"),
            lambda discussion: check_voting(discussion),
            lambda discussion : True
    ]

    new_status = 0
    for i, condition in enumerate(conditions):
        if not condition(discussion):
            new_status = i
            break
    
    if new_status != current_status:
        discussion.workflow_status = new_status
        discussion.save()
    
    
def check_stories_of_type(discussion, speech_act):
    SpeechAct = get_model("discussions", "SpeechAct")
    speech_act_obj = SpeechAct.objects.get(name=speech_act)
    model = get_model('discussions', {
        'relation': 'StoryRelation'
    }.get(speech_act_obj, 'Story'))
    elements_query = {
        'relation': lambda : model.objects.filter
    }.get(speech_act_obj, model.objects.filter)(discussion=discussion, speech_act=speech_act_obj)
    return elements_query.count()



def check_voting(discussion):
    Voting = get_model("voting", "Voting")
    return Voting.objects.filter(discussion=discussion).count()