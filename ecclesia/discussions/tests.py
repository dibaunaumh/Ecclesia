"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
import networkx as nx
from coa_discussion_actions import paths_starting_in, pick_outstanding_scores, has_path_to_nodes

class ActionsTest(TestCase):


    def test_get_paths_starting_in(self):
        """
        Tests utility method that returns all
        paths in a directed graph that start
        from a given node.
        """
        g = nx.DiGraph()
        g.add_edge(1, 5)
        g.add_edge(2, 4)
        g.add_edge(2, 5)
        g.add_edge(3, 4)
        g.add_edge(5, 6)

        expected_results_for_1 = [
            [1, 5, 6],
        ]
        
        expected_results_for_2 = [
            [2, 4],
            [2, 5, 6],
        ]

        print "Result for 1:\n", paths_starting_in(g, 1)
        print "Result for 2:\n", paths_starting_in(g, 2)

        self.failUnlessEqual(len(expected_results_for_1), len(paths_starting_in(g, 1)))
        self.failUnlessEqual(len(expected_results_for_2), len(paths_starting_in(g, 2)))


    def test_has_path_to_nodes(self):
        """
        Tests utility method that returns all
        paths in a directed graph that start
        from a given node.
        """
        g = nx.DiGraph()
        g.add_edge(1, 5)
        g.add_edge(2, 4)
        g.add_edge(2, 5)
        g.add_edge(3, 4)
        g.add_edge(5, 6)

        expected_results_for_1 = True

        expected_results_for_2 = False

        print "Result for 1:\n", has_path_to_nodes(g, 1, [5, 6])
        print "Result for 2:\n", has_path_to_nodes(g, 2, [1, 3])

        self.failUnlessEqual(expected_results_for_1, has_path_to_nodes(g, 1, [5, 6]))
        self.failUnlessEqual(expected_results_for_2, has_path_to_nodes(g, 2, [1, 3]))

    def test_pick_outstanding_scores(self):
        scores = {1: 2, 2: 4, 3: 4, 4: 4, 5: 5, 6: 5, 7: 7, 8: 9}
        expected_outstanding = [7, 8]
        actual_outstanding = pick_outstanding_scores(scores)
        self.failUnlessEqual(len(expected_outstanding), len(actual_outstanding))
        actual_outstanding.sort()
        for i, id in enumerate(expected_outstanding):
            self.failUnlessEqual(expected_outstanding[i], actual_outstanding[i])


#class DiscussionsTest(TestCase):

    #def test_delete_discussion(self):
    #    """
    #    Tests that the discussion is deleted.
    #    """
    #to do

    #def test_discussions_list(self):
    #    """
    #    Tests that the discussions list presents a correct number of discussions depending on the search and filters.
    #    """
    #to do

    #def test_delete_story(self):
    #    """
    #    Tests that the story is deleted.
    #    """
    #to do

    #def test_stories_list(self):
    #    """
    #    Tests that the stories list presents a correct number of stories depending on the search and filters.
    #    """
    #to do


