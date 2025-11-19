import random
from logging import getLogger
from typing import Union

import pytest
from common.models.subjects import Subject
from django.db import models
from django.test.client import Client
from dms.models.class_materials import Section, Topic


def check_order(collection: list[Union[Section, Topic]]):
    for i, elem in enumerate(collection):
        elem.refresh_from_db()
        assert (
            elem.order == i
        ), f"Incorrect order for {elem}: expected {i}, got {elem.order}"


def save_each(objs: list[models.Model]):
    for elem in objs:
        elem.save()


def create_section(su_client: Client, title: str, subject: Subject):
    response = su_client.post(
        "/api/dms/sections/",
        {"title": title, "subject": subject.pk},
        content_type="application/json",
    )
    assert response.status_code == 201
    created_id = response.json()["id"]
    return Section.objects.get(pk=created_id)


def move_section(su_client: Client, section: Section, position: int):
    response = su_client.patch(
        "/api/dms/sections/{}/order/".format(section.pk),
        {"to": position},
        content_type="application/json",
    )
    assert response.status_code == 200
    return response


def delete_section(su_client: Client, section: Section):
    response = su_client.delete(
        "/api/dms/sections/{}/".format(section.pk),
        content_type="application/json",
    )
    assert response.status_code == 204
    return response


def create_topic(su_client: Client, title: str, section: Section):
    response = su_client.post(
        "/api/dms/topics/",
        {"title": title, "section": section.pk},
        content_type="application/json",
    )
    assert response.status_code == 201
    created_id = response.json()["id"]
    return Topic.objects.get(pk=created_id)


def move_topic(su_client: Client, topic: Topic, position: int):
    response = su_client.patch(
        "/api/dms/topics/{}/order/".format(topic.pk),
        {"to": position},
        content_type="application/json",
    )
    assert response.status_code == 200
    return response


def delete_topic(su_client: Client, topic: Topic):
    response = su_client.delete(
        "/api/dms/topics/{}/".format(topic.pk),
        content_type="application/json",
    )
    assert response.status_code == 204
    return response


def clean_up_class_materials():
    Topic.objects.all().delete()
    Section.objects.all().delete()
    Subject.objects.all().delete()


@pytest.mark.django_db
def test_sections_creating(su_client, subject1, subject2):
    section1 = create_section(su_client, title="Section 1", subject=subject1)
    section2 = create_section(su_client, title="Section 2", subject=subject1)
    check_order([section1, section2])

    section3 = create_section(su_client, title="Section 3", subject=subject2)
    section4 = create_section(su_client, title="Section 4", subject=subject2)
    section5 = create_section(su_client, title="Section 5", subject=subject2)
    check_order([section3, section4, section5])

    clean_up_class_materials()


@pytest.mark.django_db
def test_sections_reordering(
    su_client,
    section1,
    section2,
    section3,
    section4,
    section5,
    section6,
    topic1,
    topic2,
    topic3,
    topic4,
    topic5,
    topic6,
    topic7,
    topic8,
    topic9,
):
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
    move_section(su_client=su_client, section=section4, position=0)
    check_order([section4, section1, section2, section3])
    check_order([topic6, topic7, topic1, topic2, topic3, topic4, topic5])
    check_order([section5, section6])
    check_order([topic8, topic9])

    # ------
    move_section(su_client=su_client, section=section1, position=2)
    check_order([section4, section2, section1, section3])
    check_order([topic6, topic7, topic4, topic5, topic1, topic2, topic3])
    check_order([section5, section6])
    check_order([topic8, topic9])

    # ------
    move_section(su_client=su_client, section=section4, position=2)
    check_order([section2, section1, section4, section3])
    check_order([topic4, topic5, topic1, topic2, topic3, topic6, topic7])
    check_order([section5, section6])
    check_order([topic8, topic9])

    # ------
    move_section(su_client=su_client, section=section3, position=0)
    check_order([section3, section2, section1, section4])
    check_order([topic4, topic5, topic1, topic2, topic3, topic6, topic7])
    check_order([section5, section6])
    check_order([topic8, topic9])

    # ------
    move_section(su_client=su_client, section=section3, position=2)
    check_order([section2, section1, section3, section4])
    check_order([topic4, topic5, topic1, topic2, topic3, topic6, topic7])
    check_order([section5, section6])
    check_order([topic8, topic9])

    # ------
    move_section(su_client=su_client, section=section6, position=0)
    check_order([section2, section1, section3, section4])
    check_order([topic4, topic5, topic1, topic2, topic3, topic6, topic7])
    check_order([section6, section5])
    check_order([topic9, topic8])

    clean_up_class_materials()


def random_actions(su_client, subject1, subject2):
    def get_section(sec_id: int):
        return Section.objects.filter(pk=sec_id).first()

    def get_topic(top_id: int):
        return Topic.objects.filter(pk=top_id).first()

    def get_sections_order(subj_data):
        return [get_section(s["id"]) for s in subj_data]

    def get_topics_order(subj_data):
        return [get_topic(topic["id"]) for s in subj_data for topic in s["topics"]]

    logger = getLogger()
    random.seed(42)

    s1_data = []
    s2_data = []
    sn, sn_data = subject1, s1_data
    sold, sold_data = subject2, s2_data
    for i in range(100):
        sn, sn_data, sold, sold_data = sold, sold_data, sn, sn_data
        section_order = get_sections_order(sn_data)
        topic_order = get_topics_order(sn_data)

        check_order(section_order)
        check_order(topic_order)

        actions = ["create_section"]
        if len(section_order) > 0:
            actions += ["move_section", "delete_section", "create_topic"]
        if len(topic_order) > 0:
            actions += ["move_topic", "delete_topic"]

        action = random.choice(actions)
        if action == "create_section":
            new_sec = create_section(su_client, "Section title", sn)
            sn_data.append({"id": new_sec.pk, "topics": []})
            logger.debug(f"Creating section {new_sec.pk} on subject {sn.pk}")

        elif action == "move_section":
            c_sec_order = random.randrange(len(section_order))
            to_move = random.randrange(len(section_order))
            move_section(su_client, section_order[c_sec_order], to_move)
            sn_data.insert(to_move, sn_data.pop(c_sec_order))
            logger.debug(
                f"Moving section {section_order[c_sec_order].pk} to place {to_move} on subject {sn.pk}"
            )

        elif action == "delete_section":
            c_sec_order = random.randrange(len(section_order))
            delete_section(su_client, section_order[c_sec_order])
            sn_data.pop(c_sec_order)
            logger.debug(
                f"Deleting topic {section_order[c_sec_order].pk}on subject {sn.pk}"
            )

        elif action == "create_topic":
            c_sec_order = random.randrange(len(section_order))
            new_topic = create_topic(
                su_client, "Topic title", section_order[c_sec_order]
            )
            sn_data[c_sec_order]["topics"].append({"id": new_topic.pk})
            logger.debug(
                f"Creating topic {new_topic.pk} on section {section_order[c_sec_order].pk} on subject {sn.pk}"
            )

        elif action == "move_topic":
            while 1:
                c_sec_order = random.randrange(len(section_order))
                if sn_data[c_sec_order]["topics"]:
                    break
            topic_low = sum(
                [
                    1
                    for sec_id in range(c_sec_order)
                    for top in sn_data[sec_id]["topics"]
                ]
            )
            topic_high = sum(
                [
                    1
                    for sec_id in range(c_sec_order + 1)
                    for top in sn_data[sec_id]["topics"]
                ]
            )
            assert topic_low < topic_high
            c_top_order = random.randrange(topic_low, topic_high)
            to_move = random.randrange(topic_low, topic_high)
            move_topic(su_client, topic_order[c_top_order], to_move)
            c_top_order_inside_section = c_top_order - topic_low
            to_move_inside_section = to_move - topic_low
            sn_data[c_sec_order]["topics"].insert(
                to_move_inside_section,
                sn_data[c_sec_order]["topics"].pop(c_top_order_inside_section),
            )
            logger.debug(
                f"Moving topic {topic_order[c_top_order].pk} to place {to_move}"
                f" on section {section_order[c_sec_order].pk} on subject {sn.pk}"
            )

        elif action == "delete_topic":
            while 1:
                c_sec_order = random.randrange(len(section_order))
                if sn_data[c_sec_order]["topics"]:
                    break

            topic_low = sum(
                [
                    1
                    for sec_id in range(c_sec_order)
                    for top in sn_data[sec_id]["topics"]
                ]
            )
            topic_high = sum(
                [
                    1
                    for sec_id in range(c_sec_order + 1)
                    for top in sn_data[sec_id]["topics"]
                ]
            )
            assert topic_low < topic_high
            c_top_order = random.randrange(topic_low, topic_high)
            delete_topic(su_client, topic_order[c_top_order])
            c_top_order_inside_section = c_top_order - topic_low
            sn_data[c_sec_order]["topics"].pop(c_top_order_inside_section)
            logger.debug(
                f"Deleting topic {topic_order[c_top_order].pk} "
                f"from section {section_order[c_sec_order].pk} on subject {sn.pk}"
            )
        else:
            assert False, "Incorrect action"


def test_random_actions(su_client, subject1, subject2):
    random_actions(su_client, subject1, subject2)
    clean_up_class_materials()
