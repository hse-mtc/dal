import typing as tp

from lms.models.students import Student
from lms.models.teachers import Teacher


Personnel = tp.Union[Student | Teacher]
