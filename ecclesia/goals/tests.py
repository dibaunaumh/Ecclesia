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
        
    
    def test_get_path_resolution_data(self):
        """
        Tests the goal pasth resolution data view. 
        """
        client = Client()
        for goal in self.goals:
            response = client.get("/goal/%d/data/" % goal.id)
            #expected_result = '''{"goal": {"id": %d, "name": "%s","short_description": "%s", "storiesURL":"/goal/1/stories/" },     
            #  "actions": [{"id":1,"name":"a1","storiesURL":"/stories/"},{"id":2,"name":"action2","storiesURL":"/stories/"},{"id":3,"name":"action with longer name","storiesURL":"/stories/"}],
            #  "results": [{"id":1,"name":"r1","storiesURL":"/stories/"},{"id":2,"name":"r2","storiesURL":"/stories/"},{"id":3,"name":"r3","storiesURL":"/stories/"},{"id":4,"name":"r4","storiesURL":"/stories/"}],
            #  "a2r": [{"from":1,"to":1,"storiesURL":"/stories/"},{"from":1,"to":1,"storiesURL":"/stories/"},{"from":2,"to":2,"storiesURL":"/stories/"},{"from":2,"to":3,"storiesURL":"/stories/"},{"from":3,"to":4,"storiesURL":"/stories/"}],
            #  "r2g": [{"from":1,"storiesURL":"/stories/"},{"from":2,"storiesURL":"/stories/"},{"from":3,"storiesURL":"/stories/"},{"from":4,"storiesURL":"/stories/"}]  }''' % (goal.id, goal.name, goal.short_description)
            expected_result = '''{"goal": {"id": %d, "name": "%s","short_description": "%s", "storiesURL":"/goal/1/stories/" },     
              "actions": [],
              "results": [],
              "a2r": [],
              "r2g": []  }''' % (goal.id, goal.name, goal.short_description)
            self.assertEquals(expected_result, response.content, "Path resolution data not as expected")
            


