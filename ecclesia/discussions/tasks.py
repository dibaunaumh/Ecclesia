from celery.decorators import task
from discussion_actions import evaluate_stories
from notifications.services import create_notification

@task()
def evaluate_stories_task(discussion):
    evaluate_stories(discussion)
    logger = evaluate_stories_task.get_logger()
    logger.info("Calculating evaluation for %s..." % discussion.name)

@task()
def create_notification_task(text, entity, acting_user):
    create_notification(text=text, entity=entity, acting_user=acting_user)
    logger = create_notification_task.get_logger()
    logger.info("Creating notification %s..." % text)
