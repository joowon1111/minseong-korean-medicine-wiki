import unittest
from build_archive_ai_config import public_endpoint


class AIConfigTests(unittest.TestCase):
    def test_public_endpoint(self):
        self.assertIsNone(public_endpoint(''))
        self.assertEqual(public_endpoint('https://server.example/'), 'https://server.example')
        for value in ['http://server.example', 'https://user:pass@server.example', 'https://server.example?q=1', 'https://server.example/#key', 'https://server.example:8080']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                public_endpoint(value)
