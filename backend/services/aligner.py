from difflib import SequenceMatcher
import json
import os


class FontAligner:

    def __init__(self):

        self.mapping = {}

        self.confidence = {}

    def learn(self, broken, correct):

        matcher = SequenceMatcher(
            None,
            broken,
            correct
        )

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():

            if tag != "equal":
                continue

            b = broken[i1:i2]
            c = correct[j1:j2]

            if len(b) != len(c):
                continue

            for bc, cc in zip(b, c):

                if bc not in self.mapping:

                    self.mapping[bc] = {}

                if cc not in self.mapping[bc]:

                    self.mapping[bc][cc] = 0

                self.mapping[bc][cc] += 1

    def train(self, broken_pages, ocr_pages):

        for bpage, opage in zip(
            broken_pages,
            ocr_pages
        ):

            b_lines = []

            for block in bpage["blocks"]:

                for line in block["lines"]:

                    txt = ""

                    for span in line["spans"]:

                        txt += span["text"]

                    txt = txt.strip()

                    if txt:

                        b_lines.append(txt)

            o_lines = []

            for line in opage["lines"]:

                txt = line["text"].strip()

                if txt:

                    o_lines.append(txt)

            for b, o in zip(
                b_lines,
                o_lines
            ):

                self.learn(b, o)

        return self.mapping

    def build_dictionary(self):

        final = {}

        conf = {}

        for broken in self.mapping:

            candidates = self.mapping[broken]

            total = sum(candidates.values())

            best = max(
                candidates,
                key=candidates.get
            )

            final[broken] = best

            conf[broken] = candidates[best] / total

        self.confidence = conf

        return final

    def save(self):

        os.makedirs(
            "mapping",
            exist_ok=True
        )

        with open(
            "mapping/mapping.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.build_dictionary(),
                f,
                indent=4,
                ensure_ascii=False
            )

        with open(
            "mapping/confidence.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.confidence,
                f,
                indent=4,
                ensure_ascii=False
            )