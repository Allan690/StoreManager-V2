import unittest
import json
from tests.test_basecase import TestSetUp


class UserLoginClass(TestSetUp):
    def test_admin_user_can_login(self):
        """Test if user can login"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        self.assertEqual(resp_login.status_code, 200)

    def test_attendant_user_can_be_created(self):
        """Tests if API can create attendant user"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        resp_create_user = self.app.post("/api/v2/auth/signup",
                                         data=json.dumps(dict(email="ballery@gmail.com",
                                                              password="allangmailcompany", role="attendant")),
                                         content_type="application/json",
                                         headers=auth)

        self.assertEqual(resp_create_user.status_code, 201)

    def test_error_email_missing_attendant_register(self):
        """Tests error raised when email is missing during attendant signup"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        response = self.app.post("/api/v2/auth/signup",
                                 data=json.dumps(dict(email="",
                                                      password="allangmailcompany", role="attendant")),
                                 content_type="application/json",
                                 headers=auth)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_password_with_spaces(self):
        """Tests error raised when password has spaces"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        response = self.app.post("/api/v2/auth/signup",
                                 data=json.dumps(dict(email="allan123@gmail.com",
                                                      password=" ", role="attendant")),
                                 content_type="application/json",
                                 headers=auth)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("spaces", response_msg["Message"])

    def test_password_length(self):
        """Tests that password length is equal or greater than 8"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        response = self.app.post("/api/v2/auth/signup",
                                 data=json.dumps(dict(email="allanyeye@gmail.com",
                                                      password="allan", role="attendant")),
                                 content_type="application/json",
                                 headers=auth)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("8", response_msg["Message"])

    def test_missing_password(self):
        """Tests if error is raised when password is missing."""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        response = self.app.post("/api/v2/auth/signup",
                                 data=json.dumps(dict(email="testuser2@gmail.com", password="", role="attendant")),
                                 content_type="application/json",
                                 headers=auth)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_wrong_email_format(self):
        """Tests error raised when wrong email format is provided."""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        response = self.app.post("/api/v2/auth/signup",
                                 data=json.dumps(dict(email="testuser2.gmail.com", password="asdfghjklkjhg",
                                                      role="attendant")),
                                 content_type="application/json",
                                 headers=auth)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Wrong", response_msg["Message"])

    def test_get_all_users(self):
        """Test if API can get all registered users of the app"""
        resp_login = self.app.post("/api/v2/auth/login",
                                   data=json.dumps(dict(email="allan@gmail.com",
                                                        password="allangmailcompany", role="admin")),
                                   content_type="application/json")
        result_login = json.loads(resp_login.data)
        token = result_login['token']
        auth = {"Authorization": "Bearer " + token}
        response = self.app.get('/api/v2/auth/users',
                                content_type="application/json",
                                headers=auth)
        self.assertEqual(response.status_code, 200)

    def test_valid_login_generates_auth_token(self):
        """Tests token is generated on successful login."""
        response = self.app.post("/api/v2/auth/login",
                                 data=json.dumps(dict(email="allan@gmail.com",
                                                      password="allangmailcompany", role="admin")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("token", response_msg)

if __name__ == '__main__':
    unittest.main()
