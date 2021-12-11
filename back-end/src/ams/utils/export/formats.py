from dataclasses import dataclass

from xlsxwriter.format import Format
from xlsxwriter.workbook import Workbook


# pylint: disable=too-many-instance-attributes
@dataclass
class Formats:
    header: Format
    align_center: Format
    align_left: Format
    russian_date: Format
    int: Format
    float: Format
    underline: Format
    table_center: Format
    table_center_vertical: Format
    table_name: Format
    table_date: Format

    @classmethod
    def from_workbook(cls, workbook: Workbook) -> "Formats":
        return Formats(
            header=workbook.add_format(
                {
                    "font_name": "Times New Roman",
                    "font_size": 12,
                    "bold": True,
                    "align": "center",
                }
            ),
            align_center=workbook.add_format(
                {"font_name": "Times New Roman", "font_size": 12, "align": "center"}
            ),
            align_left=workbook.add_format(
                {"font_name": "Times New Roman", "font_size": 12, "align": "left"}
            ),
            russian_date=workbook.add_format(
                {
                    "font_name": "Times New Roman",
                    "font_size": 12,
                    "num_format": "dd.mm.yyyy",
                    "border": 1,
                    "align": "center",
                    "valign": "vcenter",
                }
            ),
            int=workbook.add_format(
                {
                    "font_name": "Times New Roman",
                    "font_size": 12,
                    "align": "center",
                    "valign": "vcenter",
                    "border": 1,
                    "num_format": "#0",
                }
            ),
            float=workbook.add_format(
                {
                    "font_name": "times new roman",
                    "font_size": 12,
                    "align": "center",
                    "valign": "vcenter",
                    "border": 1,
                    "num_format": "#,##0.00",
                }
            ),
            underline=workbook.add_format(
                {
                    "font_name": "times new roman",
                    "font_size": 12,
                    "align": "left",
                    "valign": "vcenter",
                    "bottom": 1,
                }
            ),
            table_center=workbook.add_format(
                {
                    "font_name": "Times New Roman",
                    "font_size": 12,
                    "align": "center",
                    "valign": "vcenter",
                    "border": 1,
                    "text_wrap": True,
                }
            ),
            table_center_vertical=workbook.add_format(
                {
                    "font_name": "Times New Roman",
                    "font_size": 12,
                    "align": "center",
                    "valign": "vcenter",
                    "border": 1,
                    "text_wrap": True,
                    "rotation": 90,
                }
            ),
            table_name=workbook.add_format(
                {
                    "font_name": "Times New Roman",
                    "font_size": 12,
                    "align": "center",
                    "valign": "vcenter",
                    "left": 1,
                    "top": 1,
                    "bottom": 1,
                    "text_wrap": True,
                }
            ),
            table_date=workbook.add_format(
                {
                    "font_name": "Times New Roman",
                    "font_size": 12,
                    "align": "center",
                    "valign": "vcenter",
                    "right": 1,
                    "top": 1,
                    "bottom": 1,
                    "text_wrap": True,
                    "num_format": "dd.mm.yyyy",
                }
            ),
        )
