import codecs
import json
import re
from typing import List, Tuple, Dict

from hazm import Normalizer, sent_tokenize


class VehicleDetector:
    def __init__(self):
        places_data_file_locations = [
            F'data/cities.json', F'data/countries.json', F'data/provinces.json', F'data/special_place.json'
        ]
        self.places = []
        for data_file_location in places_data_file_locations:
            self.places += json.load(codecs.open(data_file_location, 'r', 'utf-8'))
        self.vehicles = json.load(codecs.open(F'data/car_names.json', 'r', 'utf-8'))
        self.vehicle_types = json.load(codecs.open(F'data/vehicle_type.json', 'r', 'utf-8'))
        self.source_stop_words = ['از']
        self.dest_stop_words = ['به', 'به سمت', 'به سوی']
        self.vehicle_stop_words = ['با', 'به وسیله', 'با خودروی']
        self.source_pattern = [self._get_stop_word_and_name_combination(self.source_stop_words, self.places)]
        self.destination_pattern = [self._get_stop_word_and_name_combination(self.dest_stop_words, self.places)]
        self.vehicle_pattern = [
            self._get_stop_word_and_name_combination(self.vehicle_stop_words, self.vehicles,
                                                     middle_names=self.vehicle_types),
            self._get_stop_word_and_name_combination(self.vehicle_stop_words, self.vehicles),
            self._get_stop_word_and_name_combination(self.vehicle_stop_words, self.vehicle_types),

        ]
        self.patterns = [
            f"{self.source_stop_words} {self.places} {self.vehicle_stop_words} {self.vehicles} {self.dest_stop_words} {self.places}"
        ]

    def _get_pattern_from_list(self, data_list):
        return "(" + "|".join(data_list) + ")"

    def _get_stop_word_and_name_combination(self, stop_words, names, middle_names=None):
        if middle_names:
            return f"{self._get_pattern_from_list(stop_words)} {self._get_pattern_from_list(names)}" \
                   f" {self._get_pattern_from_list(names)}"
        return f"{self._get_pattern_from_list(stop_words)} {self._get_pattern_from_list(names)}"

    def run(self, text: str) -> Dict[any, any]:
        sentences = self._pre_process(text)
        data = []
        for sentence in sentences:
            vehicle = self.match_vehicle(sentence)
            if vehicle:
                data.append((self.match_source(sentence), self.match_destination(sentence), vehicle))
        return self._represent_data(data)

    def _pre_process(self, text):
        normalized_text = Normalizer().normalize(text)
        sentences = sent_tokenize(normalized_text)
        # TODO: validate sentence with valid verbs.
        # lemmatizer = Lemmatizer()
        # tagger = POSTagger(model='resources/postagger.model')
        # sentences_token = [tagger.tag([lemmatizer.lemmatize(word) for word in word_tokenize(sentence)]) for sentence in
        #                    sentences]
        return sentences

    def _represent_data(self, data):
        represented_data = []
        for sample in data:
            sample_represented_data = dict()
            names = {0: "from", 1: "to", 2: "vehicle"}
            for idx in range(3):
                if sample[idx]:
                    sample_represented_data[names[idx]] = sample[idx][0].group().split(" ")[-1]
                    shift = len(" ".join(sample[idx][0].group().split(" ")[:-1])) + 1
                    sample_represented_data[names[idx] + "_span"] = [sample[idx][1] + shift, sample[idx][2]]
                else:
                    sample_represented_data[names[idx]] = ""
                    sample_represented_data[names[idx] + "_span"] = [-1, -1]

            represented_data.append(sample_represented_data)
        return represented_data

        pass

    def _match_pattern(self, patterns: List[str], text: str) -> Tuple[any, int, int]:
        finded_samples = []
        for pattern in patterns:
            for matched in re.finditer(pattern, text):
                start, end = matched.span()
                finded_samples.append((matched, start, end))
        if not finded_samples:
            return None
        return sorted(finded_samples, key=lambda item: item[2] - item[1], reverse=True)[0]

    def match_source(self, text):
        return self._match_pattern(self.source_pattern, text)

    def match_destination(self, text):
        return self._match_pattern(self.destination_pattern, text)

    def match_vehicle(self, text):
        return self._match_pattern(self.vehicle_pattern, text)
