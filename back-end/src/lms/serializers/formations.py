from rest_framework import serializers

from auth.models import Permission

from lms.models.formations import FormationReport, FormationRemark
from lms.models.teachers import Teacher
from lms.utils.functions import get_personnel_from_request_user


class FormationRemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormationRemark
        fields = [
            "id",
            "report",
            "student",
            "student_name",
            "category",
            "comment",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "student_name", "created_by", "created_at"]

    def validate(self, attrs):
        if self.instance and ("report" in attrs or "student" in attrs):
            raise serializers.ValidationError(
                "Нельзя перенести замечание в другой отчёт"
            )
        report = attrs.get("report", getattr(self.instance, "report", None))
        student = attrs.get("student", getattr(self.instance, "student", None))
        if not student:
            raise serializers.ValidationError({"student": "Выберите студента"})
        if report and student.milgroup_id != report.milgroup_id:
            raise serializers.ValidationError({"student": "Студент из другого взвода"})
        return attrs

    def create(self, validated_data):
        student = validated_data["student"]
        validated_data["student_name"] = student.fullname
        return super().create(validated_data)


class FormationReportSerializer(serializers.ModelSerializer):
    remarks = serializers.SerializerMethodField()
    milgroup_title = serializers.CharField(source="milgroup.title", read_only=True)
    milfaculty = serializers.IntegerField(
        source="milgroup.milfaculty_id", read_only=True
    )
    created_by_email = serializers.EmailField(source="created_by.email", read_only=True)
    updated_by_email = serializers.EmailField(source="updated_by.email", read_only=True)
    absent_count = serializers.SerializerMethodField()

    class Meta:
        model = FormationReport
        fields = [
            "id",
            "milgroup",
            "milgroup_title",
            "milfaculty",
            "date",
            "roster_count",
            "present_count",
            "excused_count",
            "unexcused_count",
            "unknown_count",
            "absent_count",
            "comment",
            "remarks",
            "created_by",
            "created_by_email",
            "updated_by",
            "updated_by_email",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def get_remarks(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return []
        user = request.user
        if not user.is_superuser:
            personnel = get_personnel_from_request_user(user)
            if not isinstance(personnel, Teacher):
                return []
            scope = user.get_perm_scope("formation-remarks", "get")
            if scope != Permission.Scope.ALL and not (
                scope == Permission.Scope.MILFACULTY
                and personnel.milfaculty_id == obj.milgroup.milfaculty_id
            ):
                return []
        return FormationRemarkSerializer(obj.remarks.all(), many=True).data

    def get_absent_count(self, obj):
        return obj.excused_count + obj.unexcused_count + obj.unknown_count

    def validate(self, attrs):
        if self.instance:
            for field in ("milgroup", "date"):
                if field in attrs and attrs[field] != getattr(self.instance, field):
                    raise serializers.ValidationError(
                        {field: "Нельзя изменить после создания"}
                    )
        counts = {
            field: attrs.get(field, getattr(self.instance, field, None))
            for field in (
                "roster_count",
                "present_count",
                "excused_count",
                "unexcused_count",
                "unknown_count",
            )
        }
        if all(value is not None for value in counts.values()) and (
            counts["roster_count"]
            != sum(value for field, value in counts.items() if field != "roster_count")
        ):
            raise serializers.ValidationError("Численность не сходится")
        return attrs
