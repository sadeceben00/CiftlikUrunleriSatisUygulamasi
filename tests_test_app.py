import unittest
from app import app, db, User, Product, Order

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_register(self):
        response = self.app.post('/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password',
            'role': 'tüketici'
        })
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        self.app.post('/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password',
            'role': 'tüketici'
        })
        response = self.app.post('/login', json={
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)

    def test_get_products(self):
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()