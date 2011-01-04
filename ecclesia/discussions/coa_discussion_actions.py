import template_factory
import networkx as nx
from django.db.models import get_model
import sys

TEMPLATE_NAME = "course-of-action"
COA_SPEECH_ACT = "course_of_action"
GOAL_CONDITION_SPEECH_ACT = "goal_condition"
GOAL_SPEECH_ACT = "goal"

TRUE_SPEECH_ACT = "true"
FALSE_SPEECH_ACT = "false"
GOOD_SPEECH_ACT = "good"
BAD_SPEECH_ACT = "bad"

PENALTY_FOR_NOT_ENDING_IN_GOAL = 0
ZERO_OPINION_VALUE = 0.00001

# NUMBER_OF_GROUP_MEMBERS = get_number_of_group_members(discussion)

def evaluate_stories(discussion):
    """
    Implementation of the evaluate stories discussion action
    for Course-of-Action discussions. Returns the story/stories
    having the best score.
    Stories evaluated are of Speech Act: Course-of-Action
    Evaluation formula is can be seen at: https://sites.google.com/site/ekklidev/development/design/conclusions-indication
       
    """
    conclusions = []    # list of (story_id, score) tuples
    stories = {}        

    scores = evaluate_discussion_stories(discussion, stories)

    # step 3: Pick the outstanding CoA nodes (use simple StdDev calculation)

    for coa in pick_outstanding_scores(scores):
        # print "Found conclusion: %s" % stories[coa]
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

# A function that multiply x*y
def multiply (x,y): return x*y

def evaluate_discussion_stories(discussion, stories):
    scores = {}
    evals = {}
    types = {}
    coa_stories = []
    goal_conditions = []

    # step 1: Evaluate each node & add to graph

    graph = nx.DiGraph()

    # step 1.1: loop over the relation of the discussion
    StoryRelation = get_model('discussions', 'StoryRelation')
    for rel in StoryRelation.objects.filter(discussion=discussion):
        # step 1.2: call eval_story for every node in a relation
        # relations that go to the story
        f = rel.from_story
        stories[f.id] = f
        evals[f.id] = evaluate_story(f, discussion)
        # print "evals[%s]:%s" % (f.id, evals[f.id])
        types[f.id] = f.speech_act.name
        if f.speech_act.name == COA_SPEECH_ACT and f.id not in coa_stories:
            coa_stories.append(f.id)
        elif f.speech_act.name == GOAL_CONDITION_SPEECH_ACT and f.id not in goal_conditions:
            goal_conditions.append(f.id)
        # relations that go from the story
        t = rel.to_story
        stories[t.id] = t
        evals[t.id] = evaluate_story(t, discussion)
        # print "evals[%s]:%s" % (t.id, evals[t.id])
        types[t.id] = t.speech_act.name

        # step 1.3: add the relation & its evaluated stories to a graph structure
        graph.add_edge(f.id, t.id)

    # step 2: Evaluate the graph

    # step 2.1: go over the list of CoA nodes & create a list paths starting from this CoA
    
	for coa in coa_stories:
	    # print "Coas stories: ", coa_stories 
	    # print "coa: ", coa
            paths = paths_starting_in(graph, coa)
            # print "Paths starting in CoA", coa, "are ", paths
            score = 0
            path_eval_prob=1
            total_path_eval = 0
            for p in paths:
            
                # step 2.2: calculate the aggregated evaluation of the nodes in the path
                # gets all the values of the nodes in the path
#               for s in p:
#                # print "p: ",p, " s: ",s, " evals[s]: ",evals[s], "p[2:3] = ",p[2:3]
                """
                <<  Calculate path probability by multipling all the stories (OR). >>
                Evaluating a path in https://sites.google.com/site/ekklidev/development/design/conclusions-indication
                """
            
                path_eval_ls = ([evals[s] for s in p])
                # print "path_eval_ls: ", path_eval_ls
                # multiply the gBVs of the stories in the path
                path_eval = reduce (multiply, path_eval_ls)
                # print "path_eval for",p, "is ", path_eval
                # step 2.3: check whether it ends in a Goal
                ends_in_goal = types[p[-1]] == GOAL_SPEECH_ACT
                if not ends_in_goal:
                    path_eval = 0
                total_path_eval = total_path_eval + path_eval
                # path_eval_prob=path_eval_prob*path_eval
                # print "Total path eval untill ",p, "is: ", total_path_eval
            average_path_eval = total_path_eval / len(paths)
            # print "Average paths for ",coa, "is ",average_path_eval
                        
            # scores[coa] = 1-path_eval_inv_prob
#            scores[coa] = path_eval_prob
            """
            Checks if all paths starting at the CoA are ending in the goal conditions.
            If  not ending in goal condtions then retuen zero, else return the average of the paths
            """

            
                        
            if len(goal_conditions) > 0 and not has_path_to_nodes(graph, coa, goal_conditions):
                scores[coa] = 0
                # print "CoA ", coa, "do not complay to all goal condtions."
            else:
                scores[coa] = average_path_eval
            
            scores[coa] = average_path_eval # erase after fixing
            
            # print "The score for CoA ",coa, "is ", scores[coa]
    return scores
    

def evaluate_story(story, discussion):
    try:
#        score = evaluate_truth(story, discussion) * evaluate_goodness(story, discussion)
        score = group_belief_value(discussion, story)
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
    # the function returns a list of opinions per user  
    count_by_user = {}
    for op in opinions:
        user_id = op.created_by.id
        if not user_id in count_by_user:
            count_by_user[user_id] = 1
        else:
            count_by_user[user_id] = count_by_user[user_id] + 1
    return count_by_user

def aggregate_dimension_opinions_by_users(discussion, story, positive_speech_act_name, negative_speech_act_name):

    # << The function returns a list of pBV (personal belief value) for all users. >>
    # <<The function works good, Tal 29/12/2010>>
    
    Opinion = get_model('discussions', 'Opinion')
    positive_opinions = Opinion.objects.filter(discussion=discussion, object_id=story.id, speech_act__name=positive_speech_act_name)
    negative_opinions = Opinion.objects.filter(discussion=discussion, object_id=story.id, speech_act__name=negative_speech_act_name)
    positive_count_by_user = group_opinions_by_user(positive_opinions)
    negative_count_by_user = group_opinions_by_user(negative_opinions)
    positive_count = 0

    #print positive_count_by_user
    #for user, positives in positive_count_by_user.items():
    #    if user in negative_count_by_user:
    #        negatives = negative_count_by_user[user]
    #        positive_count = float(positives) / (float(positives) + float(negatives))
    #        del negative_count_by_user[user]
    #    else:
    #        positive_count = positive_count + 1
    #negative_count = len(negative_count_by_user)
    #return (float(positive_count), float(negative_count))

    positive_opinions = list(positive_opinions)
    positive_opinions.extend(list(negative_opinions))
    opinions = positive_opinions
    
    opinion_givers = group_opinions_by_user(opinions)
    personal_belief_values = {}
    # print "Opinion Givers:", opinion_givers
    for user, opinions_count in opinion_givers.items():
        if user in positive_count_by_user:
            positives = positive_count_by_user[user]
            # print "In aggregate, user ", user, "have",  positives, "positive opinions"
        else:
            positives = 0
        personal_belief_values[user] = float(positives) / float(opinions_count)
    # print "pBVs: ",personal_belief_values
    return personal_belief_values 


def get_number_of_opinion_givers_for_story(discussion, story, positive_speech_act_name, negative_speech_act_name):
    Opinion = get_model('discussions', 'Opinion')
    opinions = Opinion.objects.filter(discussion=discussion,
                                  object_id=story.id,
                                  speech_act__name__in=(positive_speech_act_name, negative_speech_act_name))
    return len(set([opinion.created_by for opinion in opinions]))


def group_belief_value(discussion, story):

    # << The function returns average of pBVs (personal belief values) for a story >>
    #  Verified by Tal, 29/12/2010
    
    # print "story: ", story
    number_of_opinion_givers = get_number_of_opinion_givers_for_story(discussion, story, TRUE_SPEECH_ACT, FALSE_SPEECH_ACT)
    # print "number_of_opinion_givers: ", number_of_opinion_givers
    personal_belief_values = aggregate_dimension_opinions_by_users(discussion, story, TRUE_SPEECH_ACT, FALSE_SPEECH_ACT)
    ## print "True count",true_count, " and false count:", false_count
    # if no opinion, then very low probability
    #AverageTruthOpinion = (true_count / (true_count + false_count)) if (true_count + false_count) >0 else 0.00001
    number_of_group_members = get_number_of_group_members(discussion)
    print "number_of_group_members: ", number_of_group_members
    if number_of_opinion_givers > 0:
        gBV = sum(personal_belief_values.values()) / number_of_group_members
    else:
        gBV = ZERO_OPINION_VALUE
    #print "Number of group memebers", get_number_of_group_members(discussion)
    #gbv = (number_of_opinion_givers / get_number_of_group_members(discussion)) * AverageTruthOpinion
    print "In story: ", story, "gBV = ", gBV
    return gBV


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
    found = False
    for t in target_nodes:
        for p in paths:
            counter = 1
            while counter <= len(p):
                if (t == p[len(p)-counter]):
                    found = True
                    break;
                counter+=1
            if found:
                break
        if found:
            found = False
        else:
            return False
    return True

# get number og member in a discussion
def get_number_of_group_members(discussion):
    GroupProfile = get_model('groups', 'GroupProfile')
    group = GroupProfile.objects.filter(group=discussion.group)[0]
    return group.get_number_of_group_members()


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
    
