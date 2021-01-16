import api
import unittest
import json

from domain.patient import Patient


class TestDiabetesApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = api.app.test_client()
        cls.app.testing = True
        api.get_model('test')

    def test_ping(self):
        response = self.app.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), 'pong')

    def test_predict_diabetes(self):
        patient1 = Patient(1, 189, 60, 23, 846, 30.1, 0.398, 59)
        response = self.app.post('/predict', data=patient1.to_json(), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), 1)

    def test_predict_no_diabetes(self):
        patient1 = Patient(1, 189, 60, 23, 846, 30.1, 0.398, 13)
        response = self.app.post('/predict', data=patient1.to_json(), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), 0)

    def test_wrong_input(self):
        response = self.app.post('/predict', data='no json', content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_wrong_endpoint(self):
        patient = Patient(1, 189, 60, 23, 846, 30.1, 0.398, 13)
        response = self.app.post('/useless', data=patient.to_json(), content_type='application/json')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
