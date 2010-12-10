import template_factory
import networkx as nx
from django.db.models import get_model
import sys

TEMPLATE_NAME = "course-of-action"
COA_SPEECH_ACT = "course_of_action"
GOAL_SPEECH_ACT = "goal"

TRUE_SPEECH_ACT = "true"
FALSE_SPEECH_ACT = "false"
GOOD_SPEECH_ACT = "good"
BAD_SPEECH_ACT = "bad"

PENALTY_FOR_NOT_ENDING_IN_GOAL = 0

def get_number_of_group_members(discussion):
    return discussion.group.get_number_of_group_members()

def evaluate_stories(discussion):
    """
    Implementation of the evaluate stories discussion action
    for Course-of-Action discussions. Returns the story/stories
    having the best score.
    Stories evaluated are of Speech Act: Course-of-Action
    Evaluation formula is:
    score = sum( [PATH_EVAL(path) for path in discussion if path[0] = x] )
    PATH_EVAL(path) = sum( [ STORY_EVAL(story) for story in path] ) * GOAL_PROBABILITY(path)
    STORY_EVAL(story, path) = TRUE_EVAL(story, path) & GOOD_EVAL(story, path)
    TRUE_EVAL(story, path) = |True opinions| - |False opinions|
    GOOD_EVAL(story, path) = |Good opinions| - |Bad opinions|
    """
    conclusions = []    # list of (story_id, score) tuples
    stories = {}

    scores = evaluate_discussion_stories(discussion, stories)

    # step 3: Pick the outstanding CoA nodes (use simple StdDev calculation)

    for coa in pick_outstanding_scores(scores):
        print "Found conclusion: %s" % stories[coa]
        conclusions.append( (coa, int(scores[coa])) )

    # update the discussion conclusions in the database
    DiscussionConclusion = get_model('discussions', 'DiscussionConclusion')
    current = DiscussionConclusion.objects.filter(discussion=discussion.id)
    not_changed = []
    for conclusion in current:
        if (conclusion.story.id, conclusion.score) in conclusions:
            not_changed.append((conclusion.story.id, conclusion.score))
        else:
            conclusion.delete()
    for story, score in conclusions:
        if not (story, score) in not_changed:
            new_conclusion = DiscussionConclusion()
            new_conclusion.discussion = discussion
            new_conclusion.story = stories[story]
            new_conclusion.score = score
            new_conclusion.save()
    return conclusions

def multiply (x,y): return x*y

def evaluate_discussion_stories(discussion, stories):
    scores = {}
    evals = {}
    types = {}
    coa_stories = []

    # step 1: Evaluate each node & add to graph

    graph = nx.DiGraph()

    # step 1.1: loop over the relation of the discussion
    StoryRelation = get_model('discussions', 'StoryRelation')
    for rel in StoryRelation.objects.filter(discussion=discussion):
        # step 1.2: call eval_story for every node in a relation
        f = rel.from_story
        stories[f.id] = f
        evals[f.id] = evaluate_story(f, discussion)
        types[f.id] = f.speech_act.name
        if f.speech_act.name == COA_SPEECH_ACT and f.id not in coa_stories:
            coa_stories.append(f.id)
        t = rel.to_story
        stories[t.id] = t
        evals[t.id] = evaluate_story(t, discussion)
        types[t.id] = t.speech_act.name

        # step 1.3: add the relation & its evaluated stories to a graph structure
        graph.add_edge(f.id, t.id)

    # step 2: Evaluate the graph

    # step 2.1: go over the list of CoA nodes & create a list paths starting from this CoA
    for coa in coa_stories:
        paths = paths_starting_in(graph, coa)
        score = 0
        path_eval_prob=1
        
        for p in paths:
            # step 2.2: calculate the aggregated evaluation of the nodes in the path
            # gets all the values of the nodes in the path
            for s in p:
                print "p: ",p, " s: ",s, " evals[s]: ",evals[s], "p[2:3] = ",p[2:3] 
            path_eval_ls = ([evals[s] for s in p])
            path_eval = reduce (multiply, path_eval_ls)
            # step 2.3: check whether it ends in a Goal
            ends_in_goal = types[p[-1]] == GOAL_SPEECH_ACT
            if not ends_in_goal:
                path_eval = 0
            path_eval_prob=path_eval_prob*path_eval
                        
        # scores[coa] = 1-path_eval_inv_prob
        scores[coa] = path_eval_prob

    return scores
    

def evaluate_story(story, discussion):
    try:
        score = evaluate_truth(story, discussion) * evaluate_goodness(story, discussion)
        return score
    except:
        print sys.exc_info()[1]
        pass
    return 1

def evaluate_truth(story, discussion):
#    Opinion = get_model('discussions', 'Opinion')
#    true_count = float(Opinion.objects.filter(discussion=discussion, object_id=story.id, speech_act__name=TRUE_SPEECH_ACT).count())
#    false_count = float(Opinion.objects.filter(discussion=discussion, object_id=story.id, speech_act__name=FALSE_SPEECH_ACT).count())
    true_count, false_count = aggregate_dimension_opinions_by_users(discussion, story.id, TRUE_SPEECH_ACT, FALSE_SPEECH_ACT)
    # calculation should be 1, if no opinions. if only false amount of belif 0 , if some true and some false true/(true+false)
    if true_count == 0 and false_count==0:
        true_count=1
    return true_count/(true_count + false_count) 


def evaluate_goodness(story, discussion):
#    Opinion = get_model('discussions', 'Opinion')
#    good_count = float(Opinion.objects.filter(discussion=discussion, object_id=story.id, speech_act__name=GOOD_SPEECH_ACT).count())
#    bad_count = float(Opinion.objects.filter(discussion=discussion, object_id=story.id, speech_act__name=BAD_SPEECH_ACT).count())
    good_count, bad_count = aggregate_dimension_opinions_by_users(discussion, story.id, GOOD_SPEECH_ACT, BAD_SPEECH_ACT)

    if good_count == 0 and bad_count == 0: good_count=1
    eval_good = (good_count/(good_count+bad_count))
    
    if eval_good>=.5:
        x=1
    else:
        x=0
    return x


def group_opinions_by_user(opinions):
    count_by_user = {}
    for op in opinions:
        user_id = op.created_by.id
        if not user_id in count_by_user:
            count_by_user[user_id] = 1
        else:
            count_by_user[user_id] = count_by_user[user_id] + 1
    return count_by_user

def aggregate_dimension_opinions_by_users(discussion, story_id, positive_speech_act_name, negative_speech_act_name):
    Opinion = get_model('discussions', 'Opinion')
    positive_opinions = Opinion.objects.filter(discussion=discussion, object_id=story_id, speech_act__name=positive_speech_act_name)
    negative_opinions = Opinion.objects.filter(discussion=discussion, object_id=story_id, speech_act__name=negative_speech_act_name)
    positive_count_by_user = group_opinions_by_user(positive_opinions)
    negative_count_by_user = group_opinions_by_user(negative_opinions)
    positive_count = 0
    for user, positives in positive_count_by_user.items():
        if user in negative_count_by_user:
            negatives = negative_count_by_user[user]
            positive_count = float(positives) / (float(positives) + float(negatives))
            del negative_count_by_user[user]
        else:
            positive_count = positive_count + 1
    negative_count = len(negative_count_by_user)
    return (float(positive_count), float(negative_count))


#template_factory.register_discussion_action(TEMPLATE_NAME, "evaluate_stories", evaluate_stories)


# utils

def paths_starting_in(g, node, paths=None):
    """
    returns all paths in a DiGraph starting from a given node.
    TODO implement better
    """
    if paths == None:
        paths = [[node]]
    if len(g[node]) > 0:
        paths_ending_in_node = [p for p in paths if p[-1] == node]
        for p in paths_ending_in_node:
            for child, d in g[node].iteritems():
                new_p = [n for n in p]
                new_p.append(child)
                paths.append(new_p)
        for p in paths_ending_in_node:
            paths.remove(p)
        for child, d in g[node].iteritems():
            paths_starting_in(g, child, paths)
    return paths

def has_path_to_nodes(g, node, target_nodes):
    paths = paths_starting_in(g, node)
    for t in target_nodes:
        for p in paths:
            counter = 1
            while counter <= len(p):
                if (t == p[len(p)-counter]):
                    break;
                counter+=1
            if counter > len(p):
                return False
    return True

def pick_outstanding_scores(scores):
    """
    receives a dictionary of: id->score
    returns the list of ids with outstanding score,
    using simple std dev calculation.
    """
    if len(scores) == 0:
        return []
    values = scores.values()
    avg_score = sum(values) / len(values)
    squares = [(s - avg_score) ** 2 for s in values]
    stddev = int((sum(squares) / len(squares)) ** 0.5)
    return [id for id in scores.keys() if (scores[id]-avg_score) >= stddev]
    