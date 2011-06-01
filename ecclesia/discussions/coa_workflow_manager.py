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


def update_workflow_status(discussion, graph):
    """
    Check the current status & accordingly the conditions
    that change the status to a different status.
    """
    current_status = discussion.workflow_status
    if current_status == INITIAL:
            current_status = ADD_GOALS

    conditions = [
            lambda discussion: True,
            lambda discussion: check_stories_of_type(graph, "goal"),
            lambda discussion: check_stories_of_type(graph, "condition"),
            lambda discussion: check_stories_of_type(graph, "relation"),
            lambda discussion: True, #check_stories_of_type(discussion, "opinion"),
            lambda discussion: check_stories_of_type(graph, "effect"),
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
    
    
def check_stories_of_type(graph, speech_act):
    import logging
    logging.info(speech_act)
    speech_act_objects = [node for node in graph.nodes() if graph.node[node]['speech_act'] == speech_act]
    logging.info(speech_act_objects)
    return len(speech_act_objects)


def check_voting(discussion):
    Voting = get_model("voting", "Voting")
    return Voting.objects.filter(discussion=discussion).count()