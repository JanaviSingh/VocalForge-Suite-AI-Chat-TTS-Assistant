import unittest
from src.tts_module import validate_text

class TestTTSValidation(unittest.TestCase):
    def test_valid_input(self):
        valid, txt = validate_text("Hello, World!")
        self.assertTrue(valid)
        self.assertEqual(txt, "Hello, World!")

    def test_special_chars(self):
        # Should remove the @ and #
        valid, txt = validate_text("Hello @World#")
        self.assertTrue(valid)
        self.assertEqual(txt, "Hello World")

    def test_empty_input(self):
        valid, txt = validate_text("")
        self.assertFalse(valid)

if __name__ == '__main__':
    unittest.main()