import pytest
from src.modules import RUNNING_ON_PI


class TestClose:
    # @classmethod
    # def setup_class(cls):

    # def setup_method(self, method):

    @pytest.mark.skipif(RUNNING_ON_PI is False, reason="Requires running on Raspberry-Pi")
    def test_close(self, app):
        """
        Tests that macro-zero runs init's correctly
        Requires init'ing before the close
        :return:
        """
        app.init()
        result = app.close()
        assert result is True

    # def teardown_method(self, method):

    # @classmethod
    # def teardown_class(cls):
