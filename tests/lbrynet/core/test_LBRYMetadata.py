import mock
from lbrynet.core import LBRYMetadata
from lbrynet.lbrynet_daemon import LBRYExchangeRateManager

from twisted.trial import unittest


class LBRYFeeFormatTest(unittest.TestCase):
    def test_fee_created_with_correct_inputs(self):
        fee_dict = {
            'USD': {
                'amount': 10.0,
                'address': "bRcHraa8bYJZL7vkh5sNmGwPDERFUjGPP9"
            }
        }
        fee = LBRYMetadata.LBRYFeeValidator(fee_dict)
        self.assertEqual(10.0, fee['USD']['amount'])


class LBRYFeeTest(unittest.TestCase):
    def setUp(self):
        self.patcher = mock.patch('time.time')
        self.time = self.patcher.start()
        self.time.return_value = 0

    def tearDown(self):
        self.time.stop()

    def test_fee_converts_to_lbc(self):
        fee_dict = {
            'USD': {
                'amount': 10.0,
                'address': "bRcHraa8bYJZL7vkh5sNmGwPDERFUjGPP9"
            }
        }
        rates = {'BTCLBC': {'spot': 3.0, 'ts': 2}, 'USDBTC': {'spot': 2.0, 'ts': 3}}
        manager = LBRYExchangeRateManager.DummyExchangeRateManager(rates)
        self.assertEqual(60.0, manager.to_lbc(fee_dict).amount)


class MetadataTest(unittest.TestCase):
    def test_assertion_if_source_is_missing(self):
        metadata = {}
        with self.assertRaises(AssertionError):
            LBRYMetadata.Metadata(metadata)

    def test_assertion_if_invalid_source(self):
        metadata = {
            'license': 'Oscilloscope Laboratories',
            'fee': {'LBC': {'amount': 50.0, 'address': 'bRQJASJrDbFZVAvcpv3NoNWoH74LQd5JNV'}},
            'description': 'Four couples meet for Sunday brunch only to discover they are stuck in a house together as the world may be about to end.',
            'language': 'en',
            'title': "It's a Disaster",
            'author': 'Written and directed by Todd Berger',
            'sources': {
                'fake': 'source'},
            'content-type': 'audio/mpeg',
            'thumbnail': 'http://ia.media-imdb.com/images/M/MV5BMTQwNjYzMTQ0Ml5BMl5BanBnXkFtZTcwNDUzODM5Nw@@._V1_SY1000_CR0,0,673,1000_AL_.jpg'
        }
        with self.assertRaises(AssertionError):
            LBRYMetadata.Metadata(metadata)

    def test_assertion_if_missing_v001_field(self):
        metadata = {
            'license': 'Oscilloscope Laboratories',
            'fee': {'LBC': {'amount': 50.0, 'address': 'bRQJASJrDbFZVAvcpv3NoNWoH74LQd5JNV'}},
            'description': 'Four couples meet for Sunday brunch only to discover they are stuck in a house together as the world may be about to end.',
            'language': 'en',
            'author': 'Written and directed by Todd Berger',
            'sources': {
                'lbry_sd_hash': '8d0d6ea64d09f5aa90faf5807d8a761c32a27047861e06f81f41e35623a348a4b0104052161d5f89cf190f9672bc4ead'},
            'content-type': 'audio/mpeg',
            'thumbnail': 'http://ia.media-imdb.com/images/M/MV5BMTQwNjYzMTQ0Ml5BMl5BanBnXkFtZTcwNDUzODM5Nw@@._V1_SY1000_CR0,0,673,1000_AL_.jpg'
        }
        with self.assertRaises(AssertionError):
            LBRYMetadata.Metadata(metadata)

    def test_version_is_001_if_all_fields_are_present(self):
        metadata = {
            'license': 'Oscilloscope Laboratories',
            'fee': {'LBC': {'amount': 50.0, 'address': 'bRQJASJrDbFZVAvcpv3NoNWoH74LQd5JNV'}},
            'description': 'Four couples meet for Sunday brunch only to discover they are stuck in a house together as the world may be about to end.',
            'language': 'en',
            'title': "It's a Disaster",
            'author': 'Written and directed by Todd Berger',
            'sources': {
                'lbry_sd_hash': '8d0d6ea64d09f5aa90faf5807d8a761c32a27047861e06f81f41e35623a348a4b0104052161d5f89cf190f9672bc4ead'},
            'content-type': 'audio/mpeg',
            'thumbnail': 'http://ia.media-imdb.com/images/M/MV5BMTQwNjYzMTQ0Ml5BMl5BanBnXkFtZTcwNDUzODM5Nw@@._V1_SY1000_CR0,0,673,1000_AL_.jpg'
        }
        m = LBRYMetadata.Metadata(metadata)
        self.assertEquals('0.0.1', m.meta_version)

    def test_assertion_if_there_is_an_extra_field(self):
        metadata = {
            'license': 'NASA',
            'fee': {'USD': {'amount': 0.01, 'address': 'baBYSK7CqGSn5KrEmNmmQwAhBSFgo6v47z'}},
            'ver': '0.0.2',
            'description': 'SDO captures images of the sun in 10 different wavelengths, each of which helps highlight a different temperature of solar material. Different temperatures can, in turn, show specific structures on the sun such as solar flares, which are gigantic explosions of light and x-rays, or coronal loops, which are stream of solar material travelling up and down looping magnetic field lines',
            'language': 'en',
            'author': 'The SDO Team, Genna Duberstein and Scott Wiessinger',
            'title': 'Thermonuclear Art',
            'sources': {
                        'lbry_sd_hash': '8655f713819344980a9a0d67b198344e2c462c90f813e86f0c63789ab0868031f25c54d0bb31af6658e997e2041806eb'},
            'nsfw': False,
            'content-type': 'video/mp4',
            'thumbnail': 'https://svs.gsfc.nasa.gov/vis/a010000/a012000/a012034/Combined.00_08_16_17.Still004.jpg',
            'MYSTERYFIELD': '?'
        }
        with self.assertRaises(AssertionError):
            LBRYMetadata.Metadata(metadata)

    def test_version_is_002_if_all_fields_are_present(self):
        metadata = {
            'license': 'NASA',
            'fee': {'USD': {'amount': 0.01, 'address': 'baBYSK7CqGSn5KrEmNmmQwAhBSFgo6v47z'}},
            'ver': '0.0.2',
            'description': 'SDO captures images of the sun in 10 different wavelengths, each of which helps highlight a different temperature of solar material. Different temperatures can, in turn, show specific structures on the sun such as solar flares, which are gigantic explosions of light and x-rays, or coronal loops, which are stream of solar material travelling up and down looping magnetic field lines',
            'language': 'en',
            'author': 'The SDO Team, Genna Duberstein and Scott Wiessinger',
            'title': 'Thermonuclear Art',
            'sources': {
                        'lbry_sd_hash': '8655f713819344980a9a0d67b198344e2c462c90f813e86f0c63789ab0868031f25c54d0bb31af6658e997e2041806eb'},
            'nsfw': False,
            'content-type': 'video/mp4',
            'thumbnail': 'https://svs.gsfc.nasa.gov/vis/a010000/a012000/a012034/Combined.00_08_16_17.Still004.jpg'
        }
        m = LBRYMetadata.Metadata(metadata)
        self.assertEquals('0.0.2', m.meta_version)

    def test_version_claimed_is_001_but_version_is_002(self):
        metadata = {
            'license': 'NASA',
            'fee': {'USD': {'amount': 0.01, 'address': 'baBYSK7CqGSn5KrEmNmmQwAhBSFgo6v47z'}},
            'ver': '0.0.1',
            'description': 'SDO captures images of the sun in 10 different wavelengths, each of which helps highlight a different temperature of solar material. Different temperatures can, in turn, show specific structures on the sun such as solar flares, which are gigantic explosions of light and x-rays, or coronal loops, which are stream of solar material travelling up and down looping magnetic field lines',
            'language': 'en',
            'author': 'The SDO Team, Genna Duberstein and Scott Wiessinger',
            'title': 'Thermonuclear Art',
            'sources': {
                'lbry_sd_hash': '8655f713819344980a9a0d67b198344e2c462c90f813e86f0c63789ab0868031f25c54d0bb31af6658e997e2041806eb'},
            'nsfw': False,
            'content-type': 'video/mp4',
            'thumbnail': 'https://svs.gsfc.nasa.gov/vis/a010000/a012000/a012034/Combined.00_08_16_17.Still004.jpg'
        }
        with self.assertRaises(AssertionError):
            LBRYMetadata.Metadata(metadata)



