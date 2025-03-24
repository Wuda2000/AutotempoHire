import unittest
from payments.payment_module import process_payment
from payments.mpesa_api import MpesaGateway

class TestPaymentProcessing(unittest.TestCase):

    def setUp(self):
        self.user = type('User', (object,), {'phone_number': '2547XXXXXXXX'})  # Mock user object
        self.driver = type('Driver', (object,), {'available': True, 'save': lambda self: None})  # Mock driver object

    def test_successful_payment(self):
        response = process_payment(self.user, self.driver, 500, "https://yourdomain.com/mpesa/callback/", "unique_transaction_id_1")
        self.assertEqual(response['status'], 'success')
        self.assertFalse(self.driver.available)

    def test_failed_payment(self):
        response = process_payment(self.user, self.driver, 500, "https://yourdomain.com/mpesa/callback/", "unique_transaction_id_2")
        self.assertEqual(response['status'], 'error')

    def test_duplicate_transaction(self):
        process_payment(self.user, self.driver, 500, "https://yourdomain.com/mpesa/callback/", "unique_transaction_id_1")
        response = process_payment(self.user, self.driver, 500, "https://yourdomain.com/mpesa/callback/", "unique_transaction_id_1")
        self.assertEqual(response['status'], 'error')
        self.assertIn("Duplicate transaction", response['message'])

if __name__ == '__main__':
    unittest.main()
