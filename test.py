import unittest

from vehicle_detector import VehicleDetector


class TestVehicleDetector(unittest.TestCase):
    def _test_vehicle_detector_detects_correctly(self, text, expected):
        result = VehicleDetector().run(text)
        self.assertEqual(result, expected)

    def test_vehicle_detector_detects_correctly_with_simple_sentence(self):
        self._test_vehicle_detector_detects_correctly(
            text="من با قطار از تهران به اصفهان مͳ روم",
            expected=[
                {
                    "from": "تهران",
                    "from_span": [16, 20],
                    "to": "اصفهان",
                    "to_span": [20, 25],
                    "vehicle": "قطار",
                    "vehicle_span": [7, 10]
                }
            ]
        )

    def test_vehicle_detector_detects_correctly_with_complicated_sentence(self):
        self._test_vehicle_detector_detects_correctly(
            text="چون بلیت قطار پر شده بود مجبور شدم با پرایدم به تهران بروم.",
            expected=[
                {
                    "from": "",
                    "from_span": [-1, -1],
                    "to": "تهران",
                    "to_span": [50, 54],
                    "vehicle": "پراید",
                    "vehicle_span": [40, 46]
                }
            ]
        )


if __name__ == '__main__':
    unittest.main()
