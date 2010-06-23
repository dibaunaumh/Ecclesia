import template_factory
import sys
import coa_discussion_actions


def evaluate_stories(discussion):
    """
    Intended to evaluate discussion stories based on their
    support, in order to enable decision recommendation.
    Delegate to an template-specific implementation.
    """
    """
    func = template_factory.get_discussion_action(discussion.type.name, "evaluate_stories")
    if func:
        try:
            return func.__call__(discussion)
        except:
            print "Failed to evaluate stories for discussion '%s' " % discussion.name, sys.exc_info()
    """
    if discussion.type.name == "course-of-action":
        return coa_discussion_actions.evaluate_stories(discussion)
    return None