from typing_extensions import Self
from app import connex_app
import unittest
import json


class EndpointTest(unittest.TestCase):
    def test_get_director(self):
        connex_app.app.testing = True
        tester = connex_app.app.test_client(self)
        response = tester.get("api/director/7111")
        self.assertEqual(response.status_code, 200)

    def test_get_movies(self):
        connex_app.app.testing = True
        tester = connex_app.app.test_client(self)
        response = tester.get("api/movies/limit/10")
        self.assertEqual(response.status_code, 200)

    def test_post_director(self):
        payload = json.dumps(
            {"department": "Directing", "gender": 2, "name": "Fakhrul", "uid": 12434}
        )

        connex_app.app.testing = True
        tester = connex_app.app.test_client(self)
        response = tester.post(
            "api/director", headers={"Content-Type": "application/json"}, data=payload
        )
        self.assertEqual(response.status_code, 201)

    def test_get_movies_rating(self):
        connex_app.app.testing = True
        tester = connex_app.app.test_client(self)
        response = tester.get("api/movies/rating")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
