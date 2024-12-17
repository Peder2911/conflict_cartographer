
import logging
import abc

logger = logging.getLogger(__name__)

class MockDataCreator(abc.ABC):

    @property
    @abc.abstractmethod
    def Meta(self):
        pass

    @abc.abstractmethod
    def _mock(self):
        pass

    def _assert_empty(self):
        assert self.Meta.model.objects.count() == 0

    def mock(self):
        try:
            self._assert_empty()
        except AssertionError:
            logger.info(f"Skipping mocking for {self.Meta.model.__name__}: Data already exists")
        else:
            self._mock()
