import unittest
from unittest.mock import Mock
import lib.utils as utils

class TestFunctools(unittest.TestCase):
    def test_pipe(self):
        mock1 = Mock(wraps=lambda x: x + 1)
        mock2 = Mock(wraps=lambda x: x + 1)
        mock3 = Mock(wraps=lambda x: x + 1)

        test_func = utils.pipe(mock1, mock2, mock3)
        self.assertEqual(4, test_func(1))
        mock1.assert_called_with(1)
        mock2.assert_called_with(2)
        mock3.assert_called_with(3)

    def test_flow(self):
        mock1 = Mock(wraps=lambda x: x + 1)
        mock2 = Mock(wraps=lambda x: x + 1)
        mock3 = Mock(wraps=lambda x: x + 1)

        self.assertEqual(4, utils.flow(1, [mock1, mock2, mock3]))
        mock1.assert_called_with(1)
        mock2.assert_called_with(2)
        mock3.assert_called_with(3)