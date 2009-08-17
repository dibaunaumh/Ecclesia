"""
Tests the goals app services & business logic functions.
"""

from django.test import TestCase, Client
from models import *
from groups.factory import *
from common.utils import *


class GoalsTest(TestCase):
    
    groups_test = None
    user = None
    group = None
    goals = []
    actions = []
    results = []
    causing_relations = []
    leading_relations = []
    
    
    def setUp(self):
        user = create_user("__user1__", "Joe", "Doe")
        group = create_group("__group1__", user, [user,])
        self.goals.append(create_goal("__goal1__", group, user))
        self.actions.append(self.create_action("__action1__", self.goals[0]))
        self.actions.append(self.create_action("__action2__", self.goals[0]))
        self.actions.append(self.create_action("__action3__", self.goals[0]))
        self.results.append(self.create_result("__result1__", self.goals[0], True))
        self.results.append(self.create_result("__result2__", self.goals[0], True))
        self.results.append(self.create_result("__result3__", self.goals[0], False))
        self.results.append(self.create_result("__result4__", self.goals[0], True))
        self.connect_action_to_result(self.actions[0], self.results[0])
        self.connect_action_to_result(self.actions[0], self.results[1])
        self.connect_action_to_result(self.actions[1], self.results[1])
        self.connect_action_to_result(self.actions[2], self.results[2])
        
        
        
    def create_action(self, name, goal):
        action = CourseOfAction()
        action.name = name
        action.goal = goal
        action.short_description = "A test course of action"
        action.save()
        return action
    
    
    def create_result(self, name, goal, leads_to_goal=False):
        result = PossibleResult()
        result.name = name
        result.goal = goal
        result.short_description = "A test possible result"
        result.save()
        if leads_to_goal:
            rel = LeadingRelation()
            rel.possible_result = result
            rel.goal = goal
            rel.save()
        return result        
    
    
    def connect_action_to_result(self, action, result):
        rel = CausingRelation()
        rel.course_of_action = action
        rel.possible_result = result
        rel.save()
    
    
    def test_get_path_resolution_data(self):
        """
        Tests the goal pasth resolution data view. 
        """
        client = Client()
        for goal in self.goals:
            response = client.get("/goal/%d/data/" % goal.id)
            expected_result = '''{"goal": {"id": %d, "name": "%s","short_description": "%s", "storiesURL":"/goal/1/stories/" },     
              "actions": [{"id":1,"name":"__action1__","storiesURL":"/stories/"},{"id":2,"name":"__action2__","storiesURL":"/stories/"},{"id":3,"name":"__action3__","storiesURL":"/stories/"}],
              "results": [{"id":1,"name":"__result1__","storiesURL":"/stories/"},{"id":2,"name":"__result2__","storiesURL":"/stories/"},{"id":3,"name":"__result3__","storiesURL":"/stories/"},{"id":4,"name":"__result4__","storiesURL":"/stories/"}],
              "a2r": [{"from":1,"to":1,"storiesURL":"/stories/"},{"from":1,"to":2,"storiesURL":"/stories/"},{"from":2,"to":2,"storiesURL":"/stories/"},{"from":3,"to":3,"storiesURL":"/stories/"}],
              "r2g": [{"from":1,"storiesURL":"/stories/"},{"from":2,"storiesURL":"/stories/"},{"from":4,"storiesURL":"/stories/"}]  }''' % (goal.id, goal.name, goal.short_description)
            print response.content
            self.assertEquals(expected_result, response.content, "Path resolution data not as expected")
            


