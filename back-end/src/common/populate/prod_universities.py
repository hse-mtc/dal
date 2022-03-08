from common.models.universities import (
    Campus,
    Faculty,
    Program,
)

from common.utils.populate import get_or_create

import json


def add_faculties_from_file(faculties, file_name, campus):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
        for faculty in data:
            faculties.append(
                {
                    "campus": campus,
                    "title": faculty["faculty"],
                }
            )


def add_programs_from_file(programs, faculties, file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
        for program in data:
            programs.append(
                {
                    "code": program["code"],
                    "title": program["title"],
                    "faculty": faculties[program["faculty"]],
                }
            )


def create_faculties() -> dict[str, Faculty]:
    faculties = []
    files = {
        Campus.MOSCOW.value: "../data/mo-programs.json",
        Campus.NIZHNY_NOVGOROD.value: "../data/nn-programs.json",
        Campus.PERM.value: "../data/pe-programs.json",
        Campus.SAINT_PETERSBURG.value: "../data/sp-programs.json",
    }

    for key in files:
        add_faculties_from_file(faculties, files[key], key)

    return {fields["title"]: get_or_create(Faculty, **fields) for fields in faculties}


def create_programs(faculties: dict[str, Faculty]) -> dict[str, Program]:
    programs = []
    files = {
        Campus.MOSCOW.value: "../data/mo-programs.json",
        Campus.NIZHNY_NOVGOROD.value: "../data/nn-programs.json",
        Campus.PERM.value: "../data/pe-programs.json",
        Campus.SAINT_PETERSBURG.value: "../data/sp-programs.json",
    }

    for key in files:
        add_programs_from_file(programs, faculties, files[key])

    return {fields["title"]: get_or_create(Program, **fields) for fields in programs}
