
discussion_actions_by_template = {}

def register_discussion_action(template, action_name, func):
    """
    Enables a Discussion Template to register an action, that will be
    applied to discussions of this type.
    The action is any python callable.
    """
    if hasattr(func, "__call__"):
        if not discussion_actions_by_template.has_key(template):
            discussion_actions_by_template[template] = {}
        discussion_actions_by_template[template][action_name] = func


def get_discussion_action(template, action_name):
    """
    Returns a discussion action applicable for the given discussion template name,
    or None is no such action was registered.
    """
    if discussion_actions_by_template.has_key(template):
        if discussion_actions_by_template[template].has_key(action_name):
            return discussion_actions_by_template[template].get(action_name)
    return None


