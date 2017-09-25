import unittest
from pathlib2 import Path
from genty import genty, genty_dataset
from mock import MagicMock, call, patch
from zcash_cli_helper.zcli import ZCLI, ZCLIMethod


class ZCLI_tests (unittest.TestCase):
    def test_getattr(self):
        f_datadir = Path('FAKE-DATADIR')
        zcli = ZCLI(f_datadir)

        m = zcli.some_method

        self.assertIsInstance(m, ZCLIMethod)
        self.assertEqual('zcash-cli', m._execname)
        self.assertEqual(f_datadir, m._datadir)
        self.assertIs(zcli._log, m._log)


@genty
class ZCLIMethod_tests (unittest.TestCase):
    def setUp(self):
        self.m_log = MagicMock()
        self.m = ZCLIMethod('FAKE-EXEC', Path('FAKE-DATADIR'), self.m_log)

    call_rpc_argsets = dict(
        nothing=(
            [],
            [],
        ),
        strs=(
            ['a', 'b', 'c'],
            ['a', 'b', 'c'],
        ),
        jsonstuff=(
            [u'a', ['b', {'c': 'coconut'}]],
            ['"a"', '["b",{"c":"coconut"}]'],
        ),
    )

    @genty_dataset(**call_rpc_argsets)
    def test_call(self, params, expectedargs):
        with patch('subprocess.check_output') as m_check_output:
            m_check_output.return_value = 'not json object or list'

            self.m(*params)

        fullexpectedargs = [
            'FAKE-EXEC',
            '-datadir=FAKE-DATADIR',
        ] + expectedargs

        self.assertEqual(
            self.m_log.mock_calls,
            [call.debug('Running: %r', fullexpectedargs)],
        )

        self.assertEqual(
            m_check_output.mock_calls,
            [
                call(fullexpectedargs),
            ],
        )

    @genty_dataset(**call_rpc_argsets)
    def test_call_json(self, params, _):
        with patch(
                'zcash_cli_helper.zcli.ZCLIMethod._call_raw_result'
        ) as m_crr:

            # Trigger Json parsing:
            m_crr.return_value = '[]'

            with patch('zcash_cli_helper.saferjson.loads') as m_loads:
                self.m(*params)

        self.assertEqual(
            m_crr.mock_calls,
            [call(*params)],
        )

        self.assertEqual(
            m_loads.mock_calls,
            [call(m_crr.return_value)],
        )
