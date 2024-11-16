from licitpy.utils.decorators import singleton


@singleton
class SingletonClass:
    """
    Example singleton class to test the singleton decorator.
    """

    def __init__(self, value):
        self.value = value


def test_singleton_returns_same_instance():
    """
    Test that the singleton decorator ensures only one instance of a class is created.
    """
    instance1 = SingletonClass(10)
    instance2 = SingletonClass(20)

    # Both instances should be the same
    assert instance1 is instance2, "Singleton decorator should return the same instance"
    assert (
        instance1.value == 10
    ), "The value of the singleton instance should remain as initially set"


@singleton
class AnotherSingleton:
    """
    Another example singleton class to test multiple singleton instances.
    """

    def __init__(self, data):
        self.data = data


def test_different_singleton_classes():
    """
    Test that different singleton-decorated classes do not share the same instance.
    """
    instance1 = SingletonClass(5)
    instance2 = AnotherSingleton("data")

    # Instances from different singleton-decorated classes should not be the same
    assert (
        instance1 is not instance2
    ), "Singleton instances from different classes should not interfere with each other"
