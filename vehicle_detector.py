class VehicleDetector:
    def __init__(self):
        self.places = []
        self.source_stop_words = ['از']
        self.dest_stop_words = ["به"]
        self.vehicle_stop_words = ['با', 'به وسیله', ]
        self.patterns = [
            f"{self.source_stop_words} {self.places} {self.vehicle_stop_words} {self.vehicles} {self.dest_stop_words} {self.places}"
        ]


    def run(self, text: str) -> dict:
        pass
