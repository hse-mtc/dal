import datetime
import typing as tp

from pydantic import BaseModel

from campuses import Campus
from family import RelativeType


class BirthInfo(BaseModel):
    date: datetime.date
    country: str
    city: str


class ContactInfo(BaseModel):
    corporate_email: tp.Optional[str] = ""
    personal_phone_number: tp.Optional[str] = ""


class Person(BaseModel):
    surname: str
    name: str
    patronymic: tp.Optional[str] = ""

    citizenship: str
    permanent_address: str

    birth_info: BirthInfo
    contact_info: tp.Optional[ContactInfo] = None

    @property
    def full_name(self) -> str:
        name_parts = [self.surname, self.name, self.patronymic]
        return " ".join([p for p in name_parts if p])


class Relative(Person):
    type: RelativeType


class Program(BaseModel):
    code: str


class UniversityInfo(BaseModel):
    program: Program
    campus: Campus
    group: str
    card_id: str


class RecruitmentOffice(BaseModel):
    title: str
    city: tp.Optional[str] = None
    district: tp.Optional[str] = None


class Milspecialty(BaseModel):
    code: str
    milspecialty: str


class Applicant(Person):
    surname_genitive: str
    name_genitive: str
    patronymic_genitive: tp.Optional[str] = ""

    # Base64 encoded string
    photo: str

    family: list[Relative]

    university_info: UniversityInfo
    recruitment_office: RecruitmentOffice

    milspecialty: Milspecialty

