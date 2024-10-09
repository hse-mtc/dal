import pytest


@pytest.mark.django_db
def test_milspecialty_selectable(
    su_client, create_faculty, create_milspecialty, create_program
):
    cs = create_faculty(
        title="Факультет Компьютерных Наук", abbreviation="ФКН", campus="MO"
    )
    law = create_faculty(title="Юридический факультет", abbreviation="ЮФ", campus="SP")

    ami = create_program(
        title="Прикладная математика и информатика",
        code="01.03.02 Прикладная математика и информатика",
        faculty=cs,
    )
    economy = create_program(
        title="Экономика",
        code="38.03.01 Экономика",
        faculty=cs,
    )

    # SPB campus
    jurisprudence = create_program(
        title="40.03.01 Юриспруденция",
        code="40.03.01 Юриспруденция",
        faculty=law,
    )

    officers = create_milspecialty(
        title="Математическое и программное обеспечение комплексов ПРО",
        code="453100",
        selectable_by_every_program=False,
    )

    sergeants = create_milspecialty(
        title="Стрелковые, командир стрелкового отделения",
        code="100182",
        selectable_by_every_program=True,
    )

    # Allow selection of "Математическое и программное обеспечение" by ami
    officers.selectable_by.add(ami)

    # Default case (no program specified) – do not show selectable_by_program flag
    milspecialties_no_program = su_client.get(
        f"/api/lms/milspecialties/?campus={cs.campus}"
    ).json()
    for milspecialty in milspecialties_no_program:
        assert "selectable_by_program" not in milspecialty

    milspecialties_for_economy = su_client.get(
        f"/api/lms/milspecialties/?campus={cs.campus}&program={economy.pk}"
    ).json()
    assert len(milspecialties_for_economy) == 2
    golden_selectable_by_economy = {
        "453100": False,  # "Математическое и программное обеспечение" is not selectable by every program, and economy can't select it
        "100182": True,
    }
    for milspecialty in milspecialties_for_economy:
        assert milspecialty["code"] in golden_selectable_by_economy
        assert (
            milspecialty["selectable_by_program"]
            == golden_selectable_by_economy[milspecialty["code"]]
        ), f"Incorrect selectable_by_program (law) for milspecialty \"{milspecialty['title']}\""

    milspecialties_for_ami = su_client.get(
        f"/api/lms/milspecialties/?campus={cs.campus}&program={ami.pk}"
    ).json()
    assert len(milspecialties_for_ami) == 2
    golden_selectable_by_ami = {
        "453100": True,  # "Математическое и программное обеспечение" is not selectable by every program, BUT ami CAN select it
        "100182": True,
    }
    for milspecialty in milspecialties_for_ami:
        assert milspecialty["code"] in golden_selectable_by_ami
        assert (
            milspecialty["selectable_by_program"]
            == golden_selectable_by_ami[milspecialty["code"]]
        ), f"Incorrect selectable_by_program (ami) for milspecialty \"{milspecialty['title']}\""
