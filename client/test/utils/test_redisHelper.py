from utils.redis.helper import RedisHelper
from unittest import TestCase
from unittest.mock import patch


class TestRedisHelper(TestCase):
    def setUp(self):
        self.helper = RedisHelper('localhost', port=16379, password="snack.bar1", chanel="abc")

    @patch("redis.Redis")
    def test_subscribe(self, mock_obj):
        mock_obj.get_message.return_value = "123"
        self.helper._ps = mock_obj

        self.assertEqual(self.helper.get_msg(), "123")
        mock_obj.get_message.assert_called_once()
