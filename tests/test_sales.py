import json
import unittest
from tests.test_basecase import TestSetUp


class TestSalesModel(TestSetUp):
    """This class holds test cases for the sales endpoints and inherits from the TestSetUp class"""

    def test_sale_creation(self):
        """Tests whether our API can create a sale record"""
        """Create an attendant user"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(
                                       dict(email="allan@gmail.com",
                                            password="allangmailcompany")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        self.app.post("/api/v2/auth/signup",
                      data=json.dumps(dict(email="ballery112@gmail.com",
                                           password="allan121lcompany")),
                      content_type="application/json",
                      headers=auth)
        """Create a product"""
        self.app.post('/api/v2/products',
                      data=json.dumps(dict(prod_name="Bananas",
                                           prod_category="Fruits",
                                           prod_price=1200,
                                           prod_quantity=100,
                                           minimum_allowed=10,
                                           prod_description="Sweet bananas")),
                      content_type="application/json",
                      headers=auth)
        """Login the attendant and get the token"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(
                                       dict(email="ballery112@gmail.com",
                                            password="allan121lcompany",
                                            role="attendant")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth1 = {"Authorization": "Bearer " + token}
        """Create the sale"""
        response = self.app.post('/api/v2/sales',
                                 data=json.dumps(dict(prod_id=1, quantity=5)),
                                 content_type="application/json",
                                 headers=auth1)
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("created", response_msg["Message"])

    def test_sale_access_with_invalid_token(self):
        """Raise unauthorized error when invalid token is used to post a sale"""
        """Login admin user"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Use token to make a sale"""
        response = self.app.post("/api/v2/sales",
                                 data=json.dumps(dict(prod_id=1, quantity=5)),
                                 content_type="application/json",
                                 headers=auth)
        self.assertEqual(response.status_code, 401)

    def test_admin_can_get_all_sales(self):
        """Test whether API allows admin to view all sales"""
        """create a sale"""
        self.test_sale_creation()
        """Login the admin and get the token"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Get all sales"""
        resp = self.app.get('/api/v2/sales', headers=auth)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_attendant_can_only_view_their_sales(self):
        """Tests that the API allows attendant to only view their sales"""
        """create a sale"""
        self.test_sale_creation()
        """Login the attendant and get the token"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(
                                       dict(email="ballery112@gmail.com",
                                            password="allan121lcompany")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth1 = {"Authorization": "Bearer " + token}
        """View sales made"""
        resp = self.app.get('/api/v2/sales', headers=auth1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        response_msg = json.loads(resp.data.decode("UTF-8"))
        self.assertIn("Your sale was retrieved successfully", response_msg["Message"])

    def test_sale_quantity_is_zero(self):
        """Test that API should not accept zero sale quantity"""
        """Login the admin"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        self.app.post("/api/v2/auth/signup",
                      data=json.dumps(dict(email="ballery112@gmail.com",
                                           password="allan121lcompany")),
                      content_type="application/json",
                      headers=auth)
        """Create a product"""
        self.app.post('/api/v2/products',
                      data=json.dumps(dict(prod_name="Bananas",
                                           prod_category="Fruits",
                                           prod_price=1200,
                                           prod_quantity=100,
                                           minimum_allowed=10,
                                           prod_description="Sweet bananas")),
                      content_type="application/json",
                      headers=auth)
        """Login the attendant and get the token"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(
                                       dict(email="ballery112@gmail.com",
                                            password="allan121lcompany",
                                            role="attendant")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth1 = {"Authorization": "Bearer " + token}
        """Create the sale"""
        response = self.app.post('/api/v2/sales',
                                 data=json.dumps(dict(prod_id=1, quantity=0)),
                                 content_type="application/json",
                                 headers=auth1)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Quantity is required", response_msg["Message"])

    def test_prod_id_zero(self):
        """Tests that API disallows a product id of zero"""
        """Login the admin"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        self.app.post("/api/v2/auth/signup",
                      data=json.dumps(dict(email="ballery112@gmail.com",
                                           password="allan121lcompany")),
                      content_type="application/json",
                      headers=auth)
        """Create a product"""
        self.app.post('/api/v2/products',
                      data=json.dumps(dict(prod_name="Bananas",
                                           prod_category="Fruits",
                                           prod_price=1200,
                                           prod_quantity=100,
                                           minimum_allowed=10,
                                           prod_description="Sweet bananas")),
                      content_type="application/json",
                      headers=auth)
        """Login the attendant and get the token"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(
                                       dict(email="ballery112@gmail.com",
                                            password="allan121lcompany",
                                            role="attendant")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth1 = {"Authorization": "Bearer " + token}
        """Create the sale"""
        response = self.app.post('/api/v2/sales',
                                 data=json.dumps(dict(prod_id=0, quantity=10)),
                                 content_type="application/json",
                                 headers=auth1)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Product ID is required", response_msg["Message"])

    def test_prod_id_not_supplied(self):
        """Tests that the API displays an error when user fails to supply product id"""
        """Login the admin"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        self.app.post("/api/v2/auth/signup",
                      data=json.dumps(dict(email="ballery112@gmail.com",
                                           password="allan121lcompany")),
                      content_type="application/json",
                      headers=auth)
        """Create a product"""
        self.app.post('/api/v2/products',
                      data=json.dumps(dict(prod_name="Bananas",
                                           prod_category="Fruits",
                                           prod_price=1200,
                                           prod_quantity=100,
                                           minimum_allowed=10,
                                           prod_description="Sweet bananas")),
                      content_type="application/json",
                      headers=auth)
        """Login the attendant and get the token"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(
                                       dict(email="ballery112@gmail.com",
                                            password="allan121lcompany",
                                            role="attendant")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth1 = {"Authorization": "Bearer " + token}
        """Create the sale"""
        response = self.app.post('/api/v2/sales',
                                 data=json.dumps(dict(quantity=10)),
                                 content_type="application/json",
                                 headers=auth1)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Product ID is required", response_msg["Message"])

    def test_quantity_not_supplied(self):
        """Tests that the API raises an error when quantity is not supplied"""
        """Login the admin"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        self.app.post("/api/v2/auth/signup",
                      data=json.dumps(dict(email="ballery112@gmail.com",
                                           password="allan121lcompany")),
                      content_type="application/json",
                      headers=auth)
        """Create a product"""
        self.app.post('/api/v2/products',
                      data=json.dumps(dict(prod_name="Bananas",
                                           prod_category="Fruits",
                                           prod_price=1200,
                                           prod_quantity=100,
                                           minimum_allowed=10,
                                           prod_description="Sweet bananas")),
                      content_type="application/json",
                      headers=auth)
        """Login the attendant and get the token"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(
                                       dict(email="ballery112@gmail.com",
                                            password="allan121lcompany",
                                            role="attendant")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth1 = {"Authorization": "Bearer " + token}
        """Create the sale"""
        response = self.app.post('/api/v2/sales',
                                 data=json.dumps(dict(prod_id=1)),
                                 content_type="application/json",
                                 headers=auth1)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("quantity is required", response_msg["Message"])

    def test_trying_to_sale_more_than_stock(self):
        """Tests that our API prevents the user from selling more than in stock"""
        """Create an attendant user"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(
                                       dict(email="allan@gmail.com",
                                            password="allangmailcompany")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        self.app.post("/api/v2/auth/signup",
                      data=json.dumps(dict(email="ballery112@gmail.com",
                                           password="allan121lcompany")),
                      content_type="application/json",
                      headers=auth)
        """Create a product"""
        self.app.post('/api/v2/products',
                      data=json.dumps(dict(prod_name="Bananas",
                                           prod_category="Fruits",
                                           prod_price=1200,
                                           prod_quantity=100,
                                           minimum_allowed=10,
                                           prod_description="Sweet bananas")),
                      content_type="application/json",
                      headers=auth)
        """Login the attendant and get the token"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(
                                       dict(email="ballery112@gmail.com",
                                            password="allan121lcompany",
                                            role="attendant")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth1 = {"Authorization": "Bearer " + token}
        """Create the sale"""
        response = self.app.post('/api/v2/sales',
                                 data=json.dumps(dict(prod_id=1, quantity=120)),
                                 content_type="application/json",
                                 headers=auth1)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Sold quantity exceeds what is in stock", response_msg["Message"])


if __name__ == "__main__":
    unittest.main()
