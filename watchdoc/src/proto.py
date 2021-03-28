import datetime
import typing as tp

from pydantic import BaseModel

from campuses import Campus


class BirthInfo(BaseModel):
    date: datetime.date
    country: str
    city: str


class ContactInfo(BaseModel):
    corporate_email: str
    personal_phone_number: str


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


class Applicant(BaseModel):
    surname: str
    name: str
    patronymic: tp.Optional[str] = ""

    surname_genitive: str
    name_genitive: str
    patronymic_genitive: tp.Optional[str] = ""

    # Base64 encoded string
    photo: str

    birth_info: BirthInfo
    contact_info: ContactInfo
    university_info: UniversityInfo
    recruitment_office: RecruitmentOffice

    milspecialty: Milspecialty

    @property
    def full_name(self) -> str:
        name_parts = [self.surname, self.name, self.patronymic]
        return " ".join([p for p in name_parts if p])
