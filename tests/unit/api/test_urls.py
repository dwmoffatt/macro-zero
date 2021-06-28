import json


class TestURLS:
    # @classmethod
    # def setup_class(cls):

    # def setup_method(self, method):

    def test_base_url(self, client):
        response = client.get("/api/v1/hello")
        data = json.loads(response.get_data(as_text=True))
        assert data == {"message": "Hello World!!"}

    # def teardown_method(self, method):

    # @classmethod
    # def teardown_class(cls):
