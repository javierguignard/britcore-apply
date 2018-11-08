import unittest
import os
import json
from app import create_app, db


class FeatureRequestTestCase(unittest.TestCase):
    """This class represents the feature_request test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.fr = {
            'title': 'New FR',
            'description': 'This is a description',
            'client_id': 1,
            'client_priority': 1,
            'date_target': '2018-11-09',
            'product_area': 'billing',

        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    
    def test_feature_request_creation(self):
        """Test API can create a feature request (POST request)"""
        res = self.client().post(
            '/api/features_requests/',
            data=self.fr)
        self.assertEqual(res.status_code, 201)
        self.assertIn('New FR', str(res.data))


    def test_api_can_get_all_features_requests(self):
        """Test API can get a feature_request (GET request)."""
        res = self.client().post(
            '/api/features_requests/',
            data=self.fr)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/features_requests/')
        self.assertEqual(res.status_code, 200)
        print (str(res.data))
        self.assertIn('New FR', str(res.data))

    def test_api_can_get_feature_request_by_id(self):
        """Test API can get a single feature_request by using it's id."""
        rv = self.client().post(
            '/api/features_requests/',
            data=self.fr)
        self.assertEqual(rv.status_code, 201)
        results = json.loads(rv.data.decode())
        print(results['id'])
        result = self.client().get('/api/feature_requests/{}'.format(results['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('New FR', str(result.data))

    def test_feature_request_can_be_edited(self):
        """Test API can edit an existing feature_request. (PUT request)"""
        rv = self.client().post('/api/features_requests/', data=self.fr)
        self.assertEqual(rv.status_code, 201)
        # get the json with the feature_request
        results = json.loads(rv.data.decode())
        rv = self.client().put(
            '/api/feature_requests/{}'.format(results['id']),
            data={
                "title": "NEW FR ON TESTING"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get(
            '/api/feature_requests/{}'.format(results['id']))
        self.assertIn('NEW FR ON TESTING', str(results.data))

    def test_feature_request_deletion(self):
        """Test API can delete an existing feature_request. (DELETE request)."""
        rv = self.client().post('/api/features_requests/', data=self.fr)
        self.assertEqual(rv.status_code, 201)
        # get the feature_request in json
        results = json.loads(rv.data.decode())
        id_delete = results['id']
        res = self.client().delete('/api/feature_requests/{}'.format(id_delete))
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/api/feature_requests/{}'.format(id_delete))
        self.assertEqual(result.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
