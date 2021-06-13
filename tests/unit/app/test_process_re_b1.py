from src.macrozero import MacroZero, ROTARY_ENCODER_MODES, ROTARY_ENCODER_BUTTONS
from src.modules import STATUS_OK


class TestProcessREB1:
    # @classmethod
    # def setup_class(cls):

    def setup_method(self, method):
        self.app = MacroZero(test_env=True, run_webserver=False)

    def test_process_re_b1_re_mode_buttons(self):
        """
        Tests that _process_re_b1 flips rotary_encode_mode and returns OK
        rotary_encoder_mode = buttons -> modes
        :return:
        """
        self.app.rotary_encoder_mode = ROTARY_ENCODER_BUTTONS
        result = self.app._process_re_b1()
        assert self.app.rotary_encoder_mode == ROTARY_ENCODER_MODES
        assert result == STATUS_OK

    def test_process_re_b1_re_mode_modes(self):
        """
        Tests that _process_re_b1 flips rotary_encode_mode and returns OK
        rotary_encoder_mode = modes -> buttons
        :return:
        """
        self.app.rotary_encoder_mode = ROTARY_ENCODER_MODES
        result = self.app._process_re_b1()
        assert self.app.rotary_encoder_mode == ROTARY_ENCODER_BUTTONS
        assert result == STATUS_OK

    def teardown_method(self, method):
        del self.app

    # @classmethod
    # def teardown_class(cls):
