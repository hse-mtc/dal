import typing as tp

from lms.models.students import Student
from lms.models.teachers import Teacher
from ams.models.applicants import Applicant


Personnel = tp.Union[Student | Teacher | Applicant]
