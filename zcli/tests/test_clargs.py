from pathlib2 import Path
from unittest import TestCase
from mock import MagicMock, call, patch, sentinel
from zcli import clargs


class parse_args_tests (TestCase):
    @patch('argparse.ArgumentParser')
    def test_parse_args(self, m_ArgumentParser):

        class FakeOpts (object):
            def __init__(self):
                self.DATADIR = sentinel.DATADIR
                self.DEBUG = sentinel.DEBUG
                self.FAKE_ARG_A = sentinel.FAKE_ARG_A
                self.FAKE_ARG_B = sentinel.FAKE_ARG_B

        m_p = m_ArgumentParser.return_value
        m_opts = m_p.parse_args.return_value
        m_cmdclass = m_opts.cmdclass
        m_cmdclass.post_process_args.return_value = FakeOpts()

        result = clargs.parse_args(sentinel.DESCRIPTION, sentinel.ARGS)

        self.assertEqual(
            m_ArgumentParser.mock_calls[:1],
            [call(description=sentinel.DESCRIPTION)])

        self.assertEqual(
            m_ArgumentParser.mock_calls[-2:-1],
            [call().parse_args(sentinel.ARGS)])

        self.assertEqual(
            result,
            (
                {
                    'DATADIR': sentinel.DATADIR,
                    'DEBUG': sentinel.DEBUG,
                },
                m_cmdclass.run,
                {
                    'FAKE_ARG_A': sentinel.FAKE_ARG_A,
                    'FAKE_ARG_B': sentinel.FAKE_ARG_B,
                },
            )
        )

    @patch.dict('os.environ', {'ZCLI_DATADIR': 'FAKE_DATADIR'})
    def test_add_standard_args(self):
        m_argparser = MagicMock()

        result = clargs.add_standard_args(m_argparser)

        self.assertIs(None, result)

        self.assertEqual(
            m_argparser.mock_calls,
            [
                call.add_argument(
                    '--datadir',
                    dest='DATADIR',
                    type=Path,
                    default=Path('FAKE_DATADIR'),
                    help="Node datadir. Default: 'FAKE_DATADIR'",
                ),
                call.add_argument(
                    '--debug',
                    dest='DEBUG',
                    action='store_true',
                    default=False,
                    help='Debug output.',
                ),
            ])
