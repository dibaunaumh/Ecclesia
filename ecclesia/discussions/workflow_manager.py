import coa_workflow_manager

def update_workflow_status(discussion, graph):
    """
    Check the workflow status & update the discussion.
    """
    if discussion.type.name == "course-of-action":
        return coa_workflow_manager.update_workflow_status(discussion, graph)
    return None
