import pytest
from src.modules.utils import unset_bit


class TestUnsetBit:
    # @classmethod
    # def setup_class(cls):

    # def setup_method(self, method):
    #     self.app = MacroZero(test_env=True, run_webserver=False)

    def test_unset_bit_works_correctly(self):
        """
        Tests are based around 8 bit number
        - Test setting left most bit
        - Test setting right most bit
        - Test setting bit in the middle
        :return:
        """
        # Set left most bit
        value = 0b10110011
        test_value = bin(0b00110011)
        result = unset_bit(value, 7)
        assert bin(result) == test_value

        # Set right most bit
        value = 0b10110011
        test_value = bin(0b10110010)
        result = unset_bit(value, 0)
        assert bin(result) == test_value

        # Set bit in the middle
        value = 0b10110011
        test_value = bin(0b10100011)
        result = unset_bit(value, 4)
        assert bin(result) == test_value

    def test_set_bit_bit_index_must_be_int(self):
        """
        bit_index of set_bit needs to be int.
        - Test TypeError exception returned if float for bit_index
        - Test TypeError exception returned if str for bit_index
        :return:
        """

        value = 0b10110011
        bit_index = 1.1
        with pytest.raises(TypeError):
            unset_bit(value, bit_index)

        value = 0b10110011
        bit_index = 4.0
        with pytest.raises(TypeError):
            unset_bit(value, bit_index)

        value = 0b10110011
        bit_index = "3"
        with pytest.raises(TypeError):
            unset_bit(value, bit_index)

    """
    def teardown_method(self, method):
        del self.app

    @classmethod
    def teardown_class(cls):
    """
