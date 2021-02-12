import unittest
import os

from flask import Flask, render_template

from flask_compress import Compress


class DefaultsTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True

        Compress(self.app)

    def test_mimetypes_default(self):
        """ Tests COMPRESS_MIMETYPES default value is correctly set. """
        defaults = ['text/html', 'text/css', 'text/xml', 'application/json',
                    'application/javascript']
        self.assertEqual(self.app.config['COMPRESS_MIMETYPES'], defaults)

    def test_level_default(self):
        """ Tests COMPRESS_LEVEL default value is correctly set. """
        self.assertEqual(self.app.config['COMPRESS_LEVEL'], 6)

    def test_min_size_default(self):
        """ Tests COMPRESS_MIN_SIZE default value is correctly set. """
        self.assertEqual(self.app.config['COMPRESS_MIN_SIZE'], 500)

    def test_algorithm_default(self):
        """ Tests COMPRESS_ALGORITHM default value is correctly set. """
        self.assertEqual(self.app.config['COMPRESS_ALGORITHM'], ['br', 'gzip', 'deflate'])

    def test_default_deflate_settings(self):
        """ Tests COMPRESS_DELATE_LEVEL default value is correctly set. """
        self.assertEqual(self.app.config['COMPRESS_DEFLATE_LEVEL'], -1)

    def test_mode_default(self):
        """ Tests COMPRESS_BR_MODE default value is correctly set. """
        self.assertEqual(self.app.config['COMPRESS_BR_MODE'], 0)

    def test_quality_level_default(self):
        """ Tests COMPRESS_BR_LEVEL default value is correctly set. """
        self.assertEqual(self.app.config['COMPRESS_BR_LEVEL'], 4)

    def test_window_size_default(self):
        """ Tests COMPRESS_BR_WINDOW default value is correctly set. """
        self.assertEqual(self.app.config['COMPRESS_BR_WINDOW'], 22)

    def test_block_size_default(self):
        """ Tests COMPRESS_BR_BLOCK default value is correctly set. """
        self.assertEqual(self.app.config['COMPRESS_BR_BLOCK'], 0)

class InitTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True

    def test_constructor_init(self):
        Compress(self.app)

    def test_delayed_init(self):
        compress = Compress()
        compress.init_app(self.app)


class UrlTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True

        small_path = os.path.join(os.getcwd(), 'tests', 'templates',
                                  'small.html')

        large_path = os.path.join(os.getcwd(), 'tests', 'templates',
                                  'large.html')

        self.small_size = os.path.getsize(small_path) - 1
        self.large_size = os.path.getsize(large_path) - 1

        Compress(self.app)

        @self.app.route('/small/')
        def small():
            return render_template('small.html')

        @self.app.route('/large/')
        def large():
            return render_template('large.html')

    def client_get(self, ufs):
        client = self.app.test_client()
        response = client.get(ufs, headers=[('Accept-Encoding', 'gzip')])
        self.assertEqual(response.status_code, 200)
        return response

    def test_br_algorithm(self):
        client = self.app.test_client()
        headers = [('Accept-Encoding', 'br')]

        response = client.options('/small/', headers=headers)
        self.assertEqual(response.status_code, 200)

        response = client.options('/large/', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_compress_min_size(self):
        """ Tests COMPRESS_MIN_SIZE correctly affects response data. """
        response = self.client_get('/small/')
        self.assertEqual(self.small_size, len(response.data))

        response = self.client_get('/large/')
        self.assertNotEqual(self.large_size, len(response.data))

    def test_mimetype_mismatch(self):
        """ Tests if mimetype not in COMPRESS_MIMETYPES. """
        response = self.client_get('/static/1.png')
        self.assertEqual(response.mimetype, 'image/png')

    def test_content_length_options(self):
        client = self.app.test_client()
        headers = [('Accept-Encoding', 'gzip')]
        response = client.options('/small/', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_gzip_compression_level(self):
        """ Tests COMPRESS_LEVEL correctly affects response data. """
        self.app.config['COMPRESS_LEVEL'] = 1
        client = self.app.test_client()
        response = client.get('/large/', headers=[('Accept-Encoding', 'gzip')])
        response1_size = len(response.data)

        self.app.config['COMPRESS_LEVEL'] = 6
        client = self.app.test_client()
        response = client.get('/large/', headers=[('Accept-Encoding', 'gzip')])
        response6_size = len(response.data)

        self.assertNotEqual(response1_size, response6_size)

    def test_br_compression_level(self):
        """ Tests that COMPRESS_BR_LEVEL correctly affects response data. """
        self.app.config['COMPRESS_BR_LEVEL'] = 4
        client = self.app.test_client()
        response = client.get('/large/', headers=[('Accept-Encoding', 'br')])
        response4_size = len(response.data)

        self.app.config['COMPRESS_BR_LEVEL'] = 11
        client = self.app.test_client()
        response = client.get('/large/', headers=[('Accept-Encoding', 'br')])
        response11_size = len(response.data)

        self.assertNotEqual(response4_size, response11_size)

    def test_deflate_compression_level(self):
        """ Tests COMPRESS_DELATE_LEVEL correctly affects response data. """
        self.app.config['COMPRESS_DEFLATE_LEVEL'] = -1
        client = self.app.test_client()
        response = client.get('/large/', headers=[('Accept-Encoding', 'deflate')])
        response_size = len(response.data)

        self.app.config['COMPRESS_DEFLATE_LEVEL'] = 1
        client = self.app.test_client()
        response = client.get('/large/', headers=[('Accept-Encoding', 'deflate')])
        response1_size = len(response.data)

        self.assertNotEqual(response_size, response1_size)


class CompressionAlgoTests(unittest.TestCase):
    """
    Test different scenarios for compression algorithm negotiation between
    client and server. Please note that algorithm names (even the "supported"
    ones) in these tests **do not** indicate that all of these are actually
    supported by this extension.
    """
    def setUp(self):
        super(CompressionAlgoTests, self).setUp()

        # Create the app here but don't call `Compress()` on it just yet; we need
        # to be able to modify the settings in various tests. Calling `Compress(self.app)`
        # twice would result in two `@after_request` handlers, which would be bad.
        self.app = Flask(__name__)
        self.app.testing = True

        small_path = os.path.join(os.getcwd(), 'tests', 'templates', 'small.html')
        self.small_size = os.path.getsize(small_path) - 1

        @self.app.route('/small/')
        def small():
            return render_template('small.html')

    def test_setting_compress_algorithm_simple_string(self):
        """ Test that a single entry in `COMPRESS_ALGORITHM` still works for backwards compatibility """
        self.app.config['COMPRESS_ALGORITHM'] = 'gzip'
        c = Compress(self.app)
        self.assertListEqual(c.enabled_algorithms, ['gzip'])

    def test_setting_compress_algorithm_cs_string(self):
        """ Test that `COMPRESS_ALGORITHM` can be a comma-separated string """
        self.app.config['COMPRESS_ALGORITHM'] = 'gzip, br, zstd'
        c = Compress(self.app)
        self.assertListEqual(c.enabled_algorithms, ['gzip', 'br', 'zstd'])

    def test_setting_compress_algorithm_list(self):
        """ Test that `COMPRESS_ALGORITHM` can be a list of strings """
        self.app.config['COMPRESS_ALGORITHM'] = ['gzip', 'br', 'deflate']
        c = Compress(self.app)
        self.assertListEqual(c.enabled_algorithms, ['gzip', 'br', 'deflate'])

    def test_one_algo_supported(self):
        """ Tests requesting a single supported compression algorithm """
        accept_encoding = 'gzip'
        self.app.config['COMPRESS_ALGORITHM'] = ['br', 'gzip']
        c = Compress(self.app)
        self.assertEqual(c._choose_compress_algorithm(accept_encoding), 'gzip')

    def test_one_algo_unsupported(self):
        """ Tests requesting single unsupported compression algorithm """
        accept_encoding = 'some-alien-algorithm'
        self.app.config['COMPRESS_ALGORITHM'] = ['br', 'gzip']
        c = Compress(self.app)
        self.assertIsNone(c._choose_compress_algorithm(accept_encoding))

    def test_multiple_algos_supported(self):
        """ Tests requesting multiple supported compression algorithms """
        accept_encoding = 'br, gzip, zstd'
        self.app.config['COMPRESS_ALGORITHM'] = ['zstd', 'br', 'gzip']
        c = Compress(self.app)
        # When the decision is tied, we expect to see the first server-configured algorithm
        self.assertEqual(c._choose_compress_algorithm(accept_encoding), 'zstd')

    def test_multiple_algos_unsupported(self):
        """ Tests requesting multiple unsupported compression algorithms """
        accept_encoding = 'future-algo, alien-algo, forbidden-algo'
        self.app.config['COMPRESS_ALGORITHM'] = ['zstd', 'br', 'gzip']
        c = Compress(self.app)
        self.assertIsNone(c._choose_compress_algorithm(accept_encoding))

    def test_multiple_algos_with_wildcard(self):
        """ Tests requesting multiple unsupported compression algorithms and a wildcard """
        accept_encoding = 'future-algo, alien-algo, forbidden-algo, *'
        self.app.config['COMPRESS_ALGORITHM'] = ['zstd', 'br', 'gzip']
        c = Compress(self.app)
        # We expect to see the first server-configured algorithm
        self.assertEqual(c._choose_compress_algorithm(accept_encoding), 'zstd')

    def test_multiple_algos_with_different_quality(self):
        """ Tests requesting multiple supported compression algorithms with different q-factors """
        accept_encoding = 'zstd;q=0.8, br;q=0.9, gzip;q=0.5'
        self.app.config['COMPRESS_ALGORITHM'] = ['zstd', 'br', 'gzip']
        c = Compress(self.app)
        self.assertEqual(c._choose_compress_algorithm(accept_encoding), 'br')

    def test_multiple_algos_with_equal_quality(self):
        """ Tests requesting multiple supported compression algorithms with equal q-factors """
        accept_encoding = 'zstd;q=0.5, br;q=0.5, gzip;q=0.5'
        self.app.config['COMPRESS_ALGORITHM'] = ['gzip', 'br', 'zstd']
        c = Compress(self.app)
        # We expect to see the first server-configured algorithm
        self.assertEqual(c._choose_compress_algorithm(accept_encoding), 'gzip')

    def test_default_quality_is_1(self):
        """ Tests that when making mixed-quality requests, the default q-factor is 1.0 """
        accept_encoding = 'deflate, br;q=0.999, gzip;q=0.5'
        self.app.config['COMPRESS_ALGORITHM'] = ['gzip', 'br', 'deflate']
        c = Compress(self.app)
        self.assertEqual(c._choose_compress_algorithm(accept_encoding), 'deflate')

    def test_default_wildcard_quality_is_0(self):
        """ Tests that a wildcard has a default q-factor of 0.0 """
        accept_encoding = 'br;q=0.001, *'
        self.app.config['COMPRESS_ALGORITHM'] = ['gzip', 'br', 'deflate']
        c = Compress(self.app)
        self.assertEqual(c._choose_compress_algorithm(accept_encoding), 'br')

    def test_wildcard_quality(self):
        """ Tests that a wildcard with q=0 is discarded """
        accept_encoding = '*;q=0'
        self.app.config['COMPRESS_ALGORITHM'] = ['gzip', 'br', 'deflate']
        c = Compress(self.app)
        self.assertEqual(c._choose_compress_algorithm(accept_encoding), None)

    def test_identity(self):
        """ Tests that identity is understood """
        accept_encoding = 'identity;q=1, br;q=0.5, *;q=0'
        self.app.config['COMPRESS_ALGORITHM'] = ['gzip', 'br', 'deflate']
        c = Compress(self.app)
        self.assertEqual(c._choose_compress_algorithm(accept_encoding), None)

    def test_chrome_ranged_requests(self):
        """ Tests that Chrome ranged requests behave as expected """
        accept_encoding = 'identity;q=1, *;q=0'
        self.app.config['COMPRESS_ALGORITHM'] = ['gzip', 'br', 'deflate']
        c = Compress(self.app)
        self.assertEqual(c._choose_compress_algorithm(accept_encoding), None)

    def test_content_encoding_is_correct(self):
        """ Test that the `Content-Encoding` header matches the compression algorithm """
        self.app.config['COMPRESS_ALGORITHM'] = ['br', 'gzip', 'deflate']
        Compress(self.app)

        headers_gzip = [('Accept-Encoding', 'gzip')]
        client = self.app.test_client()
        response_gzip = client.options('/small/', headers=headers_gzip)
        self.assertIn('Content-Encoding', response_gzip.headers)
        self.assertEqual(response_gzip.headers.get('Content-Encoding'), 'gzip')

        headers_br = [('Accept-Encoding', 'br')]
        client = self.app.test_client()
        response_br = client.options('/small/', headers=headers_br)
        self.assertIn('Content-Encoding', response_br.headers)
        self.assertEqual(response_br.headers.get('Content-Encoding'), 'br')

        headers_deflate = [('Accept-Encoding', 'deflate')]
        client = self.app.test_client()
        response_deflate = client.options('/small/', headers=headers_deflate)
        self.assertIn('Content-Encoding', response_deflate.headers)
        self.assertEqual(response_deflate.headers.get('Content-Encoding'), 'deflate')


class CompressionPerViewTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.app.config["COMPRESS_REGISTER"] = False
        compress = Compress()
        compress.init_app(self.app)

        @self.app.route('/route1/')
        def view_1():
            return render_template('large.html')

        @self.app.route('/route2/')
        @compress.compressed()
        def view_2():
            return render_template('large.html')

    def test_compression(self):
        client = self.app.test_client()
        headers = [('Accept-Encoding', 'deflate')]

        response = client.get('/route1/', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Content-Encoding', response.headers)

        response = client.get('/route2/', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Encoding', response.headers)
        self.assertEqual(response.headers.get('Content-Encoding'), 'deflate')


if __name__ == '__main__':
    unittest.main()
