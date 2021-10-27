import argparse
import dataclasses
import json

from pathlib import Path

import docx

BASE_DIR = Path(__file__).resolve().parent


class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


@dataclasses.dataclass
class Program:
    faculty: str
    title: str
    code: str
    degree: str


def parse_programs(
    docx_path: str,
    degrees_to_ignore: list[str],
) -> list[Program]:
    programs: list[Program] = []

    document: docx.Document = docx.Document(docx_path)

    # Skip header
    rows = document.tables[0].rows[1:]

    for i, row in enumerate(rows, start=1):
        print(f"Rows with programs left: {len(rows) - i} / {len(rows)}")

        degree = row.cells[5].text.strip()

        if degree in degrees_to_ignore:
            continue

        programs.append(
            Program(
                faculty=row.cells[1].text.strip(),
                title=row.cells[3].text.strip(),
                code=row.cells[4].text.strip(),
                degree=degree,
            ))

    return programs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--programs-docx-path",
        dest="programs_docx_path",
        default=BASE_DIR / "programs.docx",
    )

    parser.add_argument(
        "--output-path",
        dest="output_path",
        default=BASE_DIR / "programs.json",
    )

    parser.add_argument(
        "--ignore-degree",
        dest="degrees_to_ignore",
        action="append",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    programs = parse_programs(
        docx_path=args.programs_docx_path,
        degrees_to_ignore=args.degrees_to_ignore,
    )
    degrees = set(program.degree for program in programs)

    print(f"Parsed {degrees = }")

    with open(args.output_path, "w") as f:
        json.dump(
            programs,
            fp=f,
            indent=2,
            ensure_ascii=False,
            cls=DataclassJSONEncoder,
        )


if __name__ == '__main__':
    main()
