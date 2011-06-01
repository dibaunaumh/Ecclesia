import template_factory
import networkx as nx
from django.db.models import get_model
import sys

TEMPLATE_NAME = "course-of-action"
COA_SPEECH_ACT = "option"
GOAL_CONDITION_SPEECH_ACT = "condition"
GOAL_SPEECH_ACT = "goal"

TRUE_SPEECH_ACT = "true"
FALSE_SPEECH_ACT = "false"
GOOD_SPEECH_ACT = "good"
BAD_SPEECH_ACT = "bad"

PENALTY_FOR_NOT_ENDING_IN_GOAL = 0
ZERO_OPINION_VALUE = 1

# NUMBER_OF_GROUP_MEMBERS = get_number_of_group_members(discussion)

def evaluate_stories(discussion, graph):
    """
    Implementation of the evaluate stories discussion action
    for Course-of-Action discussions. Returns the story/stories
    having the best score.
    Stories evaluated are of Speech Act: Course-of-Action
    Evaluation formula is can be seen at: https://sites.google.com/site/ekklidev/development/design/conclusions-indication
       
    """
    conclusions = []    # list of (story_id, score) tuples

    scores = evaluate_discussion_stories(discussion, graph)

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
            new_conclusion.story = graph.node[story]["story"]
            new_conclusion.score = score
            new_conclusion.save()
    return conclusions

# A function that multiply x*y
multiply = lambda x, y: x*y
addition = lambda x, y: x+y

def evaluate_discussion_stories(discussion, graph):
    scores = {}
    evals_t = {}
    evals_g = {}
    coa_stories = []
    goal_conditions = []

    aggregations = {}
    for node in graph.nodes():
        story = graph.node[node]["story"]
        true_false = aggregate_dimension_opinions_by_users(discussion, story, TRUE_SPEECH_ACT, FALSE_SPEECH_ACT)
        good_bad = aggregate_dimension_opinions_by_users(discussion, story, GOOD_SPEECH_ACT, BAD_SPEECH_ACT)
        aggregations[story.id] = (true_false, good_bad)
        
    # step 1: Evaluate each node & mark the Course-Of-Actions & Goal-Conditions
    for f, t in graph.edges():
        # gets the gBV and gGV of each story
        evals_t[f] = evaluate_story_truth(graph.node[f]["story"], discussion, aggregations)
        evals_g[f] = evaluate_story_goodness(graph.node[f]["story"], discussion, aggregations)

        # Add speach acts CoA and GC
        if graph.node[f]["speech_act"] == COA_SPEECH_ACT and f not in coa_stories:
            coa_stories.append(f)
        elif graph.node[f]["speech_act"] == GOAL_CONDITION_SPEECH_ACT and f not in goal_conditions:
            goal_conditions.append(f)

        evals_t[t] = evaluate_story_truth(graph.node[t]["story"], discussion, aggregations)
        evals_g[t] = evaluate_story_goodness(graph.node[t]["story"], discussion, aggregations)


    # step 2: Evaluate the graph

    # step 2.1: go over the list of CoA nodes & create a list paths starting from this CoA
    for coa in coa_stories:
        
    ########################################################################
	# Finds all the paths starting from a CoA and calculate their scores ###
	########################################################################

	
        paths = paths_starting_in(graph, coa)
            
        score = 0
        path_eval_prob=1
        total_path_eval_t = 0
        total_path_eval_g = 0
        
        
        for p in paths:
            
            # step 2.2: calculate the aggregated evaluation of the nodes in the path
            # gets all the values of the nodes in the path
#           for s in p:
#           # print "p: ",p, " s: ",s, " evals[s]: ",evals[s], "p[2:3] = ",p[2:3]
            """
            <<  Calculate path probability by multipling all the stories (OR). >>
            Evaluating a path in https://sites.google.com/site/ekklidev/development/design/conclusions-indication
            """
            
            
            path_eval_lst = [evals_t[s] for s in p]
            path_eval_lsg = [evals_g[s] for s in p]

                        
            # multiply the gBVs of the stories in the path (OR)
            path_eval_t = reduce (multiply, path_eval_lst)
            

            # Average gGVs of the stories in a path
            
            path_eval_g = (reduce (addition, path_eval_lsg))/len(p)
            
            
                        
            # step 2.3: check whether it ends in a Goal
            ends_in_goal =  graph.node[p[-1]]["speech_act"] == GOAL_SPEECH_ACT
            if not ends_in_goal:
                path_eval = 0
                
            total_path_eval_t = total_path_eval_t + path_eval_t
            total_path_eval_g = total_path_eval_g + path_eval_g
            
        # If all Goal Conditions are met then assign the average value of the paths

        #path_eval_g = total_path_eval_g/len(path_eval_lsg)
        #print "path_eval_g", path_eval_g
        
        if check_if_all_goal_conditions_met (paths, goal_conditions):
            
            average_path_eval_t = total_path_eval_t / len(paths)
            average_path_eval_g = total_path_eval_g/len(paths)
            
            average_path_eval = (total_path_eval_t / len(paths))*(total_path_eval_g/len(paths))
            
        else:
            average_path_eval = 0         
            
                      
        scores[coa] = average_path_eval # erase after fixing
            
       
    return scores
    

def evaluate_story_truth(story, discussion, aggregations):
    try:
        score = group_belief_value(discussion, story, aggregations)
        return score
    except:
        print sys.exc_info()[1]
        pass
    return 1

def evaluate_story_goodness(story, discussion, aggregations):
    try:
        score = group_goodness_value(discussion, story, aggregations)
        return score
    except:
        print sys.exc_info()[1]
        pass
    return 1

def evaluate_truth(story, discussion):

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

    positive_opinions = list(positive_opinions)
    positive_opinions.extend(list(negative_opinions))
    opinions = positive_opinions
    
    opinion_givers = group_opinions_by_user(opinions)

    personal_belief_values = {}
    for user, opinions_count in opinion_givers.items():
        if user in positive_count_by_user:
            positives = positive_count_by_user[user]
            # print "In aggregate, user ", user, "have",  positives, "positive opinions"
        else:
            positives = 0
        personal_belief_values[user] = float(positives) / float(opinions_count)
    
    return personal_belief_values 


def get_number_of_opinion_givers_for_story(discussion, story, positive_speech_act_name, negative_speech_act_name):
    Opinion = get_model('discussions', 'Opinion')
    opinions = Opinion.objects.filter(discussion=discussion,
                                  object_id=story.id,
                                  speech_act__name__in=(positive_speech_act_name, negative_speech_act_name))
    return len(set([opinion.created_by for opinion in opinions]))


def group_belief_value(discussion, story, aggregations):

    # << The function returns average of pBVs (personal belief values) for a story >>
    #  Verified by Tal, 29/12/2010
    
        
    
    number_of_opinion_givers = get_number_of_opinion_givers_for_story(discussion, story, TRUE_SPEECH_ACT, FALSE_SPEECH_ACT)

    personal_belief_values = aggregations[story][0]

    number_of_group_members = get_number_of_group_members(discussion)
    
    if number_of_opinion_givers > 0:
        
        discursersBV = (sum(personal_belief_values.values())/number_of_opinion_givers)        
        discursers_portion = float(number_of_opinion_givers) / float(number_of_group_members)
                
        gBV = discursersBV*discursers_portion
        
    else:
        gBV = ZERO_OPINION_VALUE/float(number_of_group_members)
        
    
    return gBV

# << The function returns average of pBVs (personal belief values) for a story >>
    #  Verified by Tal, 29/12/2010
    
def group_goodness_value(discussion, story, aggregations):

    number_of_opinion_givers = get_number_of_opinion_givers_for_story(discussion, story, GOOD_SPEECH_ACT, BAD_SPEECH_ACT)
    
    personal_belief_values = aggregations[story][1]
    number_of_group_members = get_number_of_group_members(discussion)
    
    
    if number_of_opinion_givers > 0:
        # good/bad are in range from -1 to +1 so we take the average of (pGV average *2)-1 to convert
        # from 0-1 scale to -1 to +1 scale
        
        discursersBV = ((sum(personal_belief_values.values())/number_of_opinion_givers)*2 )-1
        discursers_portion = float(number_of_opinion_givers) / float(number_of_group_members)

        gGV = discursersBV*discursers_portion        
    else:
        gGV = 1/float(number_of_group_members)
        
    
    # print "In story: ", story, ", gGV is", gGV
    return gGV


#template_factory.register_discussion_action(TEMPLATE_NAME, "evaluate_stories", evaluate_stories)


# utils

def check_if_all_goal_conditions_met(list,goal_conditions):
    
    gc_remove=[]
    gc_remove.extend(goal_conditions)
    
    for l in list:
        for gc in goal_conditions:
            if l.count(gc)>0:
                if gc_remove.count(gc)>0:
                    gc_remove.remove(gc)
                
    
    if gc_remove==[] and goal_conditions != []:
        return True
    else:
        return False

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
    # print "paths: ", paths
    # print "CoA: ", node
    for p in paths:
        #print "len(p): ", len (p)
        #print "path: ", p
        if len(p) >= 3:
            counter = 0
            #print "path: ", p
            while counter < len(p):
                if target_nodes == []:
                    #print "Had all the conditions"
                    return True
                if (p[counter] in target_nodes):
                    #print p[counter], "couter: ", counter
                    target_nodes.remove(p[counter])
                counter+=1
    if target_nodes == []:
        #print "Had all the conditions"
        return True
    return False
"""
def has_path_to_nodes(g, node, target_nodes):

    paths = paths_starting_in(g, node)

    found = False
    print "paths_starting", paths
    for t in target_nodes:
        print "tn: ",t
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
            print "False"
            return False
    print "True"
    return True
"""

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
    max_score = max(values)
    #avg_score = sum(values) / len(values)
    #squares = [(s - avg_score) ** 2 for s in values]
    #stddev = int((sum(squares) / len(squares)) ** 0.5)
    #return [id for id in scores.keys() if (scores[id]-avg_score) >= stddev]
    return [id for id in scores.keys() if scores[id] == max_score]

def add_node_to_graph(story, graph):
    graph.add_node(story.id, story=story, speech_act=story.speech_act.name)
    
def generate_graph(discussion):
    already_in_graph = {}
    graph = nx.DiGraph()

    # loop over the relation of the discussion
    StoryRelation = get_model('discussions', 'StoryRelation')
    for rel in StoryRelation.objects.filter(discussion=discussion):
        # call eval_story for every node in a relation
        # relations that go to the story
        f = rel.from_story
        if f.id not in already_in_graph:
            add_node_to_graph(f, graph)
            already_in_graph[f.id] = True

        # relations that go from the story
        t = rel.to_story
        if t.id not in already_in_graph:
            add_node_to_graph(t, graph)
            already_in_graph[t.id] = True

        # add the relation & its evaluated stories to a graph structure
        graph.add_edge(f.id, t.id)

    Story = get_model('discussions', 'Story')
    for story in Story.objects.filter(discussion=discussion):
        if story not in already_in_graph:
            add_node_to_graph(story, graph)

    return graph
