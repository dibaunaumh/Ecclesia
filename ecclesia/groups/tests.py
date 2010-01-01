"""
Test suite for the groups app business logic & views.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import Group, User
from models import *
from factory import *
from discussions.models import Discussion
import sys


class GroupsTest(TestCase):
    
    users = []
    members = {}
    groups = []
    discussions = {}
    
    
    def setUp(self):
        """
        Manually setup some initial fixtures. Using the fixtures/initial_data.xml is problematic, 
        because of the dependency on contrib.auth.models.Group.
        """
        # create 2 groups
        self.users.append(create_user("__user1__", "Joe", "Smith"))
        self.users.append(create_user("__user2__", "Alice", "Jones"))
        self.users.append(create_user("__user3__", "Mary", "Willson"))
        self.users.append(create_user("__user4__", "Mary", "Willson"))
        self.users.append(create_user("__user5__", "Mary", "Willson"))
        self.users.append(create_user("__user6__", "Mary", "Willson"))
        self.members["__group1__"] = [self.users[0], self.users[3],]
        self.members["__group2__"] = [self.users[1], self.users[2], self.users[3], self.users[4],]
        self.groups.append(create_group("__group1__", self.users[0], self.members["__group1__"], "_group1_"))
        self.groups.append(create_group("__group2__", self.users[1], self.members["__group2__"], "_group2_"))
        # create 3 discussions
        self.discussions["__group1__"] = [create_discussion("__discussion1.1__", self.groups[0], self.users[0], "_disc1.1_"),
                                    create_discussion("__discussion1.2__", self.groups[0], self.users[0], "_disc1.2_"),
                                    create_discussion("__discussion1.3__", self.groups[0], self.users[2], "_disc1.3_"),
                                    ]
        self.discussions["__group2__"] = [create_discussion("__discussion2.1__", self.groups[1], self.users[1], "_disc2.1_"),
                                    create_discussion("__discussion2.2__", self.groups[1], self.users[2], "_disc2.2_"),
                                    ]

    

    def test_home_page(self):
        """
        Tests that the home page presents a correct list of groups.
        """
        client = Client()
        # todo use reverse
        response = client.get("/")
        received_groups = response.context[-1]['groups']
        self.assertEquals(len(self.groups), len(received_groups), "Expected to receive %d groups, but got %d" % (len(self.groups), len(received_groups)))
        for i in range(len(self.groups)):
            self.assertEquals(self.groups[i].name, received_groups[i].name, "Expected to receive some other group name")
        
        
    def test_home_page(self):
        """
        Tests that the group home page presents a correct mission statement & lists of goals & members.
        """
        client = Client()
        # todo use reverse
        for i in range(len(self.groups)):
            response = client.get("/group/%s/" % self.groups[i].slug)
            group = response.context[-1]['group']
            self.assertEquals(self.groups[i].name, group.name, "Expected to receive some other group name")
            # test goals
            received_discussions = response.context[-1]['discussions']
            expected_discussions = self.discussions[self.groups[i].name]
            self.assertEquals(len(expected_discussions), len(received_discussions), "Expected to see a different number of discussions, found %d" % len(received_discussions))
            for j in range(len(expected_discussions)):
                self.assertEquals(expected_discussions[j].name, received_discussions[j].name, "Expected to find a different discussion name, found %s" % received_discussions[j].name)
            # test members
            received_members = response.context[-1]['members']
            expected_members = self.members[self.groups[i].name]
            self.assertEquals(len(expected_members), len(received_members), "Expected a different number of members, got %d" % len(received_members))
            for j in range(len(received_members)):
                self.assertEquals(expected_members[j].username, received_members[j].username, "Expected to find a different member name, found %s" % received_members[j].username)
        
                
        

        