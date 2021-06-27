class TestURLS:
    # @classmethod
    # def setup_class(cls):

    # def setup_method(self, method):

    def test_base_url(self, client):
        response = client.get("/")
        assert response.data == b"Hello World!!"

    # def teardown_method(self, method):

    # @classmethod
    # def teardown_class(cls):
