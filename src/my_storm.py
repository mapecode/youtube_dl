# pylint: disable=C0114
import IceStorm
import color
ORCHESTRATOR_TOPIC_NAME = 'OrchestratorSync'
DOWNLOADER_TOPIC_NAME = 'UpdateEvents'


def get_topic_manager(broker):
    """
    Function for create a topic manager
    @param broker:
    @return: topic manager
    """
    key = 'IceStorm.TopicManager.Proxy'
    topic_manager_proxy = broker.propertyToProxy(key)

    if topic_manager_proxy is None:
        raise ValueError("property {} not set".format(key))
    # pylint: disable=E1101
    topic_manager = IceStorm.TopicManagerPrx.checkedCast(topic_manager_proxy)

    if not topic_manager:
        raise ValueError(color.BOLD + color.RED + 'Invalid proxy in topic manager' + color.END)

    return topic_manager


def get_topic(topic_manager, topic_name):
    """
    Function for generate the topic
    @param topic_manager: the topic manager for create the topic
    @param topic_name: the topic name
    @return: topic
    """
    try:
        return topic_manager.retrieve(topic_name)
    # pylint: disable=E1101
    except IceStorm.NoSuchTopic:
        return topic_manager.create(topic_name)
