import unittest

from vehicle_detector import VehicleDetector


class TestVehicleDetector(unittest.TestCase):
    def _test_vehicle_detector_detects_correctly(self, text, expected):
        result = VehicleDetector().run(text)
        self.assertEqual(result, expected)

    def test_vehicle_detector_detects_correctly_with_simple_sentence_1(self):
        self._test_vehicle_detector_detects_correctly(
            text="من با قطار از تهران به اصفهان مͳ روم",
            expected=[
                {
                    "from": "تهران",
                    "from_span": [14, 19],
                    "to": "اصفهان",
                    "to_span": [23, 29],
                    "vehicle": "قطار",
                    "vehicle_span": [6, 10]
                }
            ]
        )

    def test_vehicle_detector_detects_correctly_with_sentence_2(self):
        self._test_vehicle_detector_detects_correctly(
            text="چون بلیت قطار پر شده بود مجبور شدم با پرایدم به تهران بروم.",
            expected=[
                {
                    "from": "",
                    "from_span": [-1, -1],
                    "to": "تهران",
                    "to_span": [48, 53],
                    "vehicle": "پراید",
                    "vehicle_span": [38, 43]
                }
            ]
        )

    def test_vehicle_detector_detects_correctly_with_sentence_3(self):
        self._test_vehicle_detector_detects_correctly(
            text="از تهران با ماشین های پردودش خوشم نیامده و به شهرهای حومه آن بیشتر علاقه دارم",
            expected=[]
        )

    def test_vehicle_detector_detects_correctly_with_sentence_4(self):
        self._test_vehicle_detector_detects_correctly(
            text="● من و خواهرم تیبا معمولا با هواپیما مسافرت مͳ کنیم.",
            expected=[
                {
                    "from": "",
                    "from_span": [-1, -1],
                    "to": "",
                    "to_span": [-1, -1],
                    "vehicle": "هواپیما",
                    "vehicle_span": [29, 36]
                }
            ]
        )
    def test_vehicle_detector_detects_correctly_with_sentence_5(self):
        self._test_vehicle_detector_detects_correctly(
            text="در حال رانندگی با خودروی تیبا هستم.",
            expected=[
                {
                    "from": "",
                    "from_span": [-1, -1],
                    "to": "",
                    "to_span": [-1, -1],
                    "vehicle": "تیبا",
                    "vehicle_span": [25, 29]
                }
            ]
        )


if __name__ == '__main__':
    unittest.main()
