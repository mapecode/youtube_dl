import IceStorm
import color
ORCHESTRATOR_TOPIC_NAME = 'OrchestratorSync'
DOWNLOADER_TOPIC_NAME = 'UpdateEvents'


def get_topic_manager(broker):
    key = 'IceStorm.TopicManager.Proxy'
    topic_manager_proxy = broker.propertyToProxy(key)

    if topic_manager_proxy is None:
        raise ValueError("property {} not set".format(key))

    topic_manager = IceStorm.TopicManagerPrx.checkedCast(topic_manager_proxy)

    if not topic_manager:
        raise ValueError(color.BOLD + color.RED + 'Invalid proxy in topic manager' + color.END)

    return topic_manager


def get_topic(topic_manager, topic):
    try:
        return topic_manager.retrieve(topic)
    except IceStorm.NoSuchTopic:
        return topic_manager.create(topic)
