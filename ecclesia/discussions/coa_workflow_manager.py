from django.db.models import get_model


# CoA workflow status
# IMPORTANT: when editing this list, be sure to edit also the corresponding messages in coa_workflow_hints.py
NOT_ALLOWED_TO_EDIT = -1
INITIAL = 0
ADD_GOALS = 1
ADD_CONDITIONS = 2
ADD_RELATIONS_FROM_CONDITIONS_TO_GOALS = 3
ADD_OPTIONS = 4
ADD_EFFECTS = 5
ADD_RELATIONS_FROM_OPTIONS_TO_EFFECTS = 6
ADD_RELATIONS_FROM_EFFECTS_TO_CONDITIONS = 7
ADD_OPINIONS_ON_STORIES = 8
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
            lambda discussion: check_stories_of_speech_act(graph, "goal"),
            lambda discussion: check_stories_of_speech_act(graph, "condition"),
            lambda discussion: check_relations_between(graph, "condition", "goal"),
            lambda discussion: check_stories_of_speech_act(graph, "option"),
            lambda discussion: check_stories_of_speech_act(graph, "effect"),
            lambda discussion: check_relations_between(graph, "option", "effect"),
            lambda discussion: check_relations_between(graph, "effect", "condition"),
            lambda discussion: check_opinions(discussion),
            lambda discussion: check_voting(discussion),
            lambda discussion : True
    ]

    new_status = 0
    reached_status = 0
    for i, condition in enumerate(conditions):
        if not condition(discussion):
            new_status = i
            break
        else:
            reached_status = i
            
    if reached_status > new_status:
        new_status = reached_status
    
    if new_status != current_status:
        discussion.workflow_status = new_status
        discussion.save()
    

def check_relations_between(graph, from_speech_act, to_speech_act):
    count = 0
    for f, t in graph.edges():
        if graph.node[f]['speech_act'] == from_speech_act and graph.node[t]['speech_act'] == to_speech_act:
            count += 1
    return count


def check_stories_of_speech_act(graph, speech_act):
    import logging
    logging.info(speech_act)
    speech_act_objects = [node for node in graph.nodes() if graph.node[node]['speech_act'] == speech_act]
    logging.info(speech_act_objects)
    return len(speech_act_objects)



def check_opinions(discussion):
    Opinion = get_model("discussions", "Opinion")
    return Opinion.objects.filter(discussion=discussion).count()

def check_voting(discussion):
    Voting = get_model("voting", "Voting")
    return Voting.objects.filter(discussion=discussion).count()