import json
import unittest
from tests.test_basecase import TestSetUp


class TestProductModel(TestSetUp):
    """This class holds test cases for the products endpoints"""

    def test_product_creation(self):
        """Tests whether our API can create a product"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        response = self.app.post('/api/v2/products',
                                 data=json.dumps(dict(prod_name="Bananas", prod_category="Fruits", prod_price=1200,
                                                      prod_quantity=100, minimum_allowed=10,
                                                      prod_description="Sweet bananas")),
                                 content_type="application/json",
                                 headers=auth)
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Product", response_msg["Message"])

    def test_product_access_with_invalid_token(self):
        """Raise unauthorized error when invalid token is used"""
        """Login the admin"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth1 = {"Authorization": "Bearer " + token}
        """Sign up an attendant"""
        resp_create_user = self.app.post("/api/v2/auth/signup",
                                         data=json.dumps(dict(email="ballery112@gmail.com",
                                                              password="allan121lcompany", role="attendant")),
                                         content_type="application/json",
                                         headers=auth1)
        """Login the attendant"""
        self.assertEqual(resp_create_user.status_code, 201)
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="ballery112@gmail.com",
                                                        password="allan121lcompany", role="attendant")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Try to use attendant's token to create a product"""
        response = self.app.post("/api/v2/products",
                                 data=json.dumps(dict(prod_name="Mangoes", prod_category="Fruits", prod_price=1200,
                                                      prod_quantity=100, minimum_allowed=10,
                                                      prod_description="Sweet bananas")),
                                 content_type="application/json",
                                 headers=auth)
        self.assertEqual(response.status_code, 401)

    def test_find_product_by_id(self):
        """Tests whether our API can find a product by its id"""
        """create the product"""
        self.test_product_creation()
        """login a user"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Find a product by id"""
        resp = self.app.get('/api/v2/products/1', headers=auth)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_get_all_products(self):
        """Test whether API can list all products in the database"""
        """create a product"""
        self.test_product_creation()
        """Login the user"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Fetch all items in the database"""
        resp = self.app.get('/api/v2/products', headers=auth)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_missing_product_name(self):
        """Test that API should not accept missing product name"""
        """Login a user"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Post a product without name"""
        response = self.app.post("/api/v2/products",
                                 data=json.dumps(dict(prod_name="", prod_category="Fruits", prod_price=1200,
                                                      prod_quantity=100, minimum_allowed=10,
                                                      prod_description="Sweet bananas")),
                                 content_type="application/json",
                                 headers=auth)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_missing_product_descr(self):
        """Test that API should not accept missing product description"""
        """Login a user"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Add a product without description"""
        response = self.app.post("/api/v2/products",
                                 data=json.dumps(dict(prod_name="Bananas", prod_category="Fruits", prod_price=1200,
                                                      prod_quantity=100, minimum_allowed=10,
                                                      prod_description="")),
                                 content_type="application/json",
                                 headers=auth)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_missing_category(self):
        """Test that API should not accept missing product category"""
        """Login a user"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Add a product without category"""
        response = self.app.post("/api/v2/products",
                                 data=json.dumps(dict(prod_name="Bananas", prod_category="", prod_price=1200,
                                                      prod_quantity=100, minimum_allowed=10,
                                                      prod_description="Sweet bananas")),
                                 content_type="application/json",
                                 headers=auth)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_product_price_string(self):
        """"Tests that the API should not accept product price as a string"""
        """Login the user"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Try posting a product with price as string"""
        response = self.app.post("/api/v2/products",
                                 data=json.dumps(dict(prod_name="Bananas", prod_category="Fruits", prod_price="1200",
                                                      prod_quantity=100, minimum_allowed=10,
                                                      prod_description="Sweet bananas")),
                                 content_type="application/json",
                                 headers=auth)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("number", response_msg["Message"])

    def test_quantity_string(self):
        """Tests that the API should not accept quantities that are strings"""
        """Login the user"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Add a product with quantity as string"""
        response = self.app.post("/api/v2/products",
                                 data=json.dumps(dict(prod_name="Bananas", prod_category="Fruits", prod_price=1200,
                                                      prod_quantity="100", minimum_allowed=10,
                                                      prod_description="Sweet bananas")),
                                 content_type="application/json",
                                 headers=auth)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("number", response_msg["Message"])

    def test_min_allowed_string(self):
        """Tests that the API should not accept minimum allowed quantity as a string"""
        """Login the user"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Add a product with min allowed quantity as string"""
        response = self.app.post("/api/v2/products",
                                 data=json.dumps(dict(prod_name="Bananas", prod_category="Fruits", prod_price=1200,
                                                      prod_quantity=100, minimum_allowed="10",
                                                      prod_description="Sweet bananas")),
                                 content_type="application/json",
                                 headers=auth)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("number", response_msg["Message"])

    def test_product_update(self):
        """Tests that the API can update a product"""
        """Create a product"""
        self.test_product_creation()
        """Login the admin user and get token"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Update the product"""
        response = self.app.put("/api/v2/products/1",
                                data=json.dumps(dict(prod_name="Apples", prod_category="Fruits", prod_price=1200,
                                                     prod_quantity=100, minimum_allowed=10,
                                                     prod_description="Sweet bananas")),
                                content_type="application/json",
                                headers=auth)
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("updated", response_msg["Message"])

    def test_product_update_unauthorized_user(self):
        """Tests that the API prevents an unauthorized user from updating a product"""
        """Create a product"""
        self.test_product_creation()
        """Login the admin"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth1 = {"Authorization": "Bearer " + token}
        """Sign up an attendant"""
        resp_create_user = self.app.post("/api/v2/auth/signup",
                                         data=json.dumps(dict(email="ballery112@gmail.com",
                                                              password="allan121lcompany", role="attendant")),
                                         content_type="application/json",
                                         headers=auth1)
        """Login the attendant"""
        self.assertEqual(resp_create_user.status_code, 201)
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="ballery112@gmail.com",
                                                        password="allan121lcompany", role="attendant")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Try to update product using attendant's token"""
        response = self.app.put("/api/v2/products/1",
                                data=json.dumps(dict(prod_name="Apples", prod_category="Fruits", prod_price=1200,
                                                     prod_quantity=100, minimum_allowed=10,
                                                     prod_description="Sweet bananas")),
                                content_type="application/json",
                                headers=auth)
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("admin", response_msg["Message"])

    def test_product_delete(self):
        """Tests that the API can delete a product."""
        """create a product"""
        self.test_product_creation()
        """Login the admin user and get token"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Delete the product"""
        response = self.app.delete("/api/v2/products/1",
                                   content_type="application/json",
                                   headers=auth)
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("deleted", response_msg["Message"])

    def test_invalid_delete_request(self):
        """Tests that the API raises an error when user places an invalid delete request"""
        """create a product"""
        self.test_product_creation()
        """Login the admin user and get token"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Try to delete non-existent product"""
        response = self.app.delete("/api/v2/products/28",
                                   content_type="application/json",
                                   headers=auth)
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_unauthorized_delete(self):
        """Tests that API prevents unauthorized user from deleting a product"""
        """create a product"""
        self.test_product_creation()
        """Login the admin user and get token"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Sign up an attendant"""
        resp_create_user = self.app.post("/api/v2/auth/signup",
                                         data=json.dumps(dict(email="ballery112@gmail.com",
                                                              password="allan121lcompany", role="attendant")),
                                         content_type="application/json",
                                         headers=auth)
        """Login the attendant"""
        self.assertEqual(resp_create_user.status_code, 201)
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="ballery112@gmail.com",
                                                        password="allan121lcompany", role="attendant")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth1 = {"Authorization": "Bearer " + token}
        """Try deleting a product with attendant's token"""
        response = self.app.delete("/api/v2/products/1",
                                   content_type="application/json",
                                   headers=auth1)
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("must be an admin", response_msg["Message"])

    def test_for_non_duplicates(self):
        """Tests that API raises an error if you try to add a
         product that is in the  database"""
        """create a product"""
        self.test_product_creation()
        """Login the admin user and get token"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        """Try to add the same product you already created"""
        response = self.app.post("/api/v2/products",
                                 data=json.dumps(dict(prod_name="Bananas", prod_category="Fruits", prod_price=1200,
                                                      prod_quantity=100, minimum_allowed=10,
                                                      prod_description="Sweet bananas")),
                                 content_type="application/json",
                                 headers=auth)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("already exists", response_msg["Message"])


if __name__ == "__main__":
    unittest.main()
