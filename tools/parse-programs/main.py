import argparse
import dataclasses
import json

from pathlib import Path

import docx

BASE_DIR = Path(__file__).resolve().parent

COLUMNS_IN_TABLE_BY_DEFAULT = 7


class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def clean_ws(s: str) -> str:
    s = s.strip()
    s = s.replace('\n', ' ')
    s = " ".join(s.split())
    return s


def remove_hse(s: str) -> str:
    hse = "Национального исследовательского университета «Высшая школа экономики»"
    s = s.replace(hse, "")
    return s


def tidy(s: str) -> str:
    s = clean_ws(s)
    s = remove_hse(s)
    s = clean_ws(s)
    return s


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
        cells = [tidy(c.text) for c in row.cells]

        if len(cells) != COLUMNS_IN_TABLE_BY_DEFAULT:
            print(f"Skipping bad program: {cells = }")
            continue

        print(f"\rPrograms left: {len(rows) - i} / {len(rows)}", end="")

        degree: str = cells[5].lower()

        if degree in degrees_to_ignore:
            continue

        programs.append(
            Program(
                faculty=cells[1],
                title=cells[3],
                code=cells[4],
                degree=degree.title(),
            ))

    print()

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
        default=[],
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not Path(args.programs_docx_path).exists():
        print(f"File with programs `{args.programs_docx_path}` does not exist, bailing out")
        exit(1)

    programs = parse_programs(
        docx_path=args.programs_docx_path,
        degrees_to_ignore=[
            degree.lower() for degree in args.degrees_to_ignore
        ],
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
