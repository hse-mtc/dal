from typing import Union

from django.test.client import Client

import pytest

from common.models.milspecialties import Milspecialty
from common.models.subjects import Subject
from dms.models.class_materials import Section, Topic
from django.db import models


def check_order(collection: list[Union[Section, Topic]]):
    for i, elem in enumerate(collection):
        elem.refresh_from_db()
        assert elem.order == i, f"Incorrect order for {elem}: expected {i}, got {elem.order}"


def save_each(objs: list[models.Model]):
    for elem in objs:
        elem.save()


def create_section(su_client: Client, title: str, subject: Section):
    response = su_client.post(
        "/api/dms/sections/",
        {"title": title, "subject": subject.pk},
        content_type="application/json",
    )
    assert response.status_code == 200
    return response


def move_section(su_client: Client, section: Section, position: int):
    response = su_client.patch(
        "/api/dms/sections/{}/order/".format(section.pk),
        {"to": position},
        content_type="application/json",
    )
    assert response.status_code == 200
    return response


@pytest.mark.django_db
def test_sections_creating(su_client):
    ms1 = Milspecialty(title="Test milspec", code="123456", available_for=["MO"])
    save_each([ms1])
    subject1 = Subject(title="Subject 1", annotation="Annotation for subject 1", milspecialty=ms1)
    subject2 = Subject(title="Subject 2", annotation="Annotation for subject 2", milspecialty=ms1)
    save_each([subject1, subject2])


@pytest.mark.django_db
def test_sections_reordering(su_client):
    ms1 = Milspecialty(title="Test milspec", code="123456", available_for=["MO"])
    save_each([ms1])
    subject1 = Subject(title="Subject 1", annotation="Annotation for subject 1", milspecialty=ms1)
    subject2 = Subject(title="Subject 2", annotation="Annotation for subject 2", milspecialty=ms1)
    save_each([subject1, subject2])

    section1 = Section(title="Section 1", subject=subject1)
    section2 = Section(title="Section 2", subject=subject1)
    section3 = Section(title="Section 3", subject=subject1)
    section4 = Section(title="Section 3", subject=subject1)
    section5 = Section(title="Section 4", subject=subject2)
    section6 = Section(title="Section 5", subject=subject2)
    save_each([section1, section2, section3, section4, section5, section6])

    topic1 = Topic(title="Topic 1", annotation="Annotation for topic 1", section=section1)
    topic2 = Topic(title="Topic 2", annotation="Annotation for topic 2", section=section1)
    topic3 = Topic(title="Topic 3", annotation="Annotation for topic 3", section=section1)
    topic4 = Topic(title="Topic 4", annotation="Annotation for topic 4", section=section2)
    topic5 = Topic(title="Topic 5", annotation="Annotation for topic 5", section=section2)
    topic6 = Topic(title="Topic 6", annotation="Annotation for topic 6", section=section3)
    topic7 = Topic(title="Topic 7", annotation="Annotation for topic 7", section=section3)
    topic8 = Topic(title="Topic 8", annotation="Annotation for topic 8", section=section5)
    topic9 = Topic(title="Topic 9", annotation="Annotation for topic 9", section=section6)

    save_each([topic1, topic2, topic3, topic4, topic5, topic6, topic7, topic8, topic9])

    # ------

    # Subject 1:
    #   Section 1:
    #     Topic 1
    #     Topic 2
    #     Topic 3
    #   Section 2:
    #     Topic 4
    #     Topic 5
    #   Section 3:
    #     Topic 6
    #     Topic 7
    #   Section 4:
    # Subject 2:
    #   Section 4:
    #     Topic 8
    #   Section 5:
    #     Topic 9

    check_order([section1, section2, section3, section4])
    check_order([topic1, topic2, topic3, topic4, topic5, topic6, topic7])
    check_order([section5, section6])
    check_order([topic8, topic9])

    # ------
    move_section(su_client=su_client, section=section1, position=0)  # Nothing changed
    check_order([section1, section2, section3, section4])
    check_order([topic1, topic2, topic3, topic4, topic5, topic6, topic7])
    check_order([section5, section6])
    check_order([topic8, topic9])

    # ------
    move_section(su_client=su_client, section=section1, position=1)
    check_order([section2, section1, section3, section4])
    check_order([topic4, topic5, topic1, topic2, topic3, topic6, topic7])
    check_order([section5, section6])
    check_order([topic8, topic9])

    # ------
    move_section(su_client=su_client, section=section1, position=1)  # nothing changed
    check_order([section2, section1, section3, section4])
    check_order([topic4, topic5, topic1, topic2, topic3, topic6, topic7])
    check_order([section5, section6])
    check_order([topic8, topic9])

    # ------
    move_section(su_client=su_client, section=section2, position=1)
    check_order([section1, section2, section3, section4])
    check_order([topic1, topic2, topic3, topic4, topic5, topic6, topic7])
    check_order([section5, section6])
    check_order([topic8, topic9])

    # ------
    move_section(su_client=su_client, section=section3, position=0)
    check_order([section3, section1, section2, section4])
    check_order([topic6, topic7, topic1, topic2, topic3, topic4, topic5])
    check_order([section5, section6])
    check_order([topic8, topic9])

    # ------
    move_section(su_client=su_client, section=section1, position=2)
    check_order([section3, section2, section1, section4])
    check_order([topic6, topic7, topic4, topic5, topic1, topic2, topic3])
    check_order([section5, section6])
    check_order([topic8, topic9])

    # ------
    move_section(su_client=su_client, section=section3, position=2)
    check_order([section2, section1, section3, section4])
    check_order([topic4, topic5, topic1, topic2, topic3, topic6, topic7])
    check_order([section5, section6])
    check_order([topic8, topic9])

    # ------
    move_section(su_client=su_client, section=section4, position=0)
    check_order([section4, section2, section1, section3])
    check_order([topic4, topic5, topic1, topic2, topic3, topic6, topic7])
    check_order([section5, section6])
    check_order([topic8, topic9])

    # ------
    move_section(su_client=su_client, section=section4, position=2)
    check_order([section2, section1, section4, section3])
    check_order([topic4, topic5, topic1, topic2, topic3, topic6, topic7])
    check_order([section5, section6])
    check_order([topic8, topic9])

    # ------
    move_section(su_client=su_client, section=section6, position=0)
    check_order([section2, section1, section4, section3])
    check_order([topic4, topic5, topic1, topic2, topic3, topic6, topic7])
    check_order([section6, section5])
    check_order([topic9, topic8])

