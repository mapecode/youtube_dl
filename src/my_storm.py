import IceStorm

ORCHESTRATOR_TOPIC_NAME = 'OrchestratorSync'
DOWNLOADER_TOPIC_NAME = 'UpdateEvents'
EXCEPTION = IceStorm.NoSuchTopic


def get_topic_manager(broker):
    key = 'IceStorm.TopicManager.Proxy'
    topic_manager_proxy = broker.propertyToProxy(key)

    if topic_manager_proxy is None:
        raise ValueError("property {} not set".format(key))

    return IceStorm.TopicManagerPrx.checkedCast(topic_manager_proxy)
