#!/usr/bin/env python3
"""
fill_prod.py — Вариант 2 (prod) заполнения "Протокола конкурсного отбора".

Заливает физподготовку (ФИЗО) ДОСЛОВНО через ручку ручного ввода и средний балл
в DAL API по HTTP, после чего DAL заново экспортирует протокол. Итоговые числа
берутся из ЕДИНОГО общего модуля tools/dal-fill/core.py (тот же, что использует
ручной Вариант 1), поэтому оба пути обязаны дать идентичный протокол.

Что делает:
  1. Аутентификация: POST email+password на /api/auth/tokens/obtain/
     (можно передать готовый --token).
  2. Список абитуриентов с заявками (пагинация) через
     GET /api/ams/applicants/applications/?campus=... — строит карту
     normalized(name, dob) -> {id, mean_grade, aggregates, existing exercise_results}.
  3. Физподготовка (ДОСЛОВНО, без пересчёта) через ручку override:
       POST /api/ams/applicants/{id}/exercise-results/override/
       {results:[{exercise_type, value, secondary_score, extra_params}...],
        strength_score, speed_score, endurance_score, physical_test_grade}
     Балл secondary_score и агрегаты пишутся как есть (это числа комиссии).
  4. Средний балл — политика fill-empty-plus-report-conflicts:
       PATCH /api/ams/applicants/{id}/application/ {mean_grade: committee_value}
       ТОЛЬКО если mean_grade в БД == 0/пусто. Иначе, если отличается — конфликт
       (пишем в отчёт), НЕ перезаписываем.

Замечание по маппингу: core отдаёт exercise_results как
{exercise_type, value_to_store, secondary_score, extra_params}; ручка override
ждёт {exercise_type, value, secondary_score, extra_params}. value_to_store -> value.

БЕЗОПАСНОСТЬ:
  * По умолчанию DRY-RUN: без --execute сервер НЕ мутируется. Реальный прогон по
    проду — РУЧНОЙ шаг пользователя. Скрипт лишь готовит и печатает план.
  * В dry-run печатается полный PLAN (JSON) и пишется в
    ~/Downloads/dal-fill-db/artifacts/prod/plan.json.
  * Идемпотентно/resumable: override заменяет весь набор результатов; grade —
    fill-empty по факту текущего состояния (перечитывается каждый прогон).

Примеры запуска:
  # Собрать план из xlsx БЕЗ HTTP (мок карты абитуриентов из имён ФИЗО):
  python3 tools/dal-fill/fill_prod.py --self-check

  # Dry-run против сервера (читает, но НЕ пишет); печатает и сохраняет план:
  python3 tools/dal-fill/fill_prod.py --base-url http://localhost:1112 \
      --email admin@mail.ru --password secret

  # Реально записать (РУЧНОЙ шаг пользователя):
  python3 tools/dal-fill/fill_prod.py --base-url https://dal.example \
      --token "$JWT" --execute
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

# Импорт общего модуля (лежит рядом).
sys.path.insert(0, str(Path(__file__).resolve().parent))
import core  # noqa: E402

# ---------------------------------------------------------------------------
# Константы путей / API
# ---------------------------------------------------------------------------
ARTIFACTS_DIR = core.DATA / "artifacts" / "prod"
PLAN_PATH = ARTIFACTS_DIR / "plan.json"

DEFAULT_BASE_URL = "http://localhost:1112"

TOKEN_OBTAIN_PATH = "/api/auth/tokens/obtain/"
APPLICATIONS_PATH = "/api/ams/applicants/applications/"


def _override_path(applicant_id) -> str:
    return f"/api/ams/applicants/{applicant_id}/exercise-results/override/"


def _application_path(applicant_id) -> str:
    return f"/api/ams/applicants/{applicant_id}/application/"


# Кампусы физподготовки: только Москва + ВАВТ (в ведомости нет СПб/НН/Перми).
PHYSICAL_CAMPUSES = ["MO", "VA"]


# ===========================================================================
# HTTP-клиент
# ===========================================================================
class DalClient:
    """Тонкий requests-клиент к DAL API.

    Никогда не выполняет мутирующих запросов, если execute=False:
    POST/PATCH возвращают синтетический ответ-заглушку (dry-run).
    """

    def __init__(self, base_url: str, token: str | None = None,
                 execute: bool = False, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.execute = execute
        self.timeout = timeout
        self.session = requests.Session()
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    # ---- auth -----------------------------------------------------------
    def obtain_token(self, email: str, password: str) -> str:
        """POST email+password -> access-токен; ставит Authorization header."""
        url = self.base_url + TOKEN_OBTAIN_PATH
        resp = self.session.post(
            url, json={"email": email, "password": password}, timeout=self.timeout
        )
        resp.raise_for_status()
        data = resp.json()
        token = data.get("access") or data.get("access_token")
        if not token:
            raise RuntimeError(f"No access token in response: {data!r}")
        self.session.headers["Authorization"] = f"Bearer {token}"
        return token

    # ---- read -----------------------------------------------------------
    def list_applications(self, campus: str, page_size: int = 200):
        """Итерирует всех абитуриентов кампуса (следует пагинации DRF)."""
        url = self.base_url + APPLICATIONS_PATH
        params = {"campus": campus, "page_size": page_size}
        while url:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict) and "results" in data:
                yield from data["results"]
                url = data.get("next")
                params = None  # next уже содержит query
            else:  # непагинированный ответ
                yield from data
                url = None

    # ---- write (гейтятся через execute) --------------------------------
    def override_physical(self, applicant_id, body: dict) -> dict:
        """POST на ручку override — дословная заливка физ. результатов."""
        url = self.base_url + _override_path(applicant_id)
        if not self.execute:
            return {"_dry_run": True, "method": "POST", "url": url, "body": body}
        resp = self.session.post(url, json=body, timeout=self.timeout)
        resp.raise_for_status()
        return {"status_code": resp.status_code}

    def patch_application(self, applicant_id, body: dict) -> dict:
        url = self.base_url + _application_path(applicant_id)
        if not self.execute:
            return {"_dry_run": True, "method": "PATCH", "url": url, "body": body}
        resp = self.session.patch(url, json=body, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()


# ===========================================================================
# Построение карты абитуриентов из ответа API (или мока)
# ===========================================================================
def _applicant_record_from_api(item: dict) -> dict:
    """Нормализовать один элемент /applicants/applications/ в запись карты."""
    ap = item.get("application_process") or {}
    existing = {}
    for er in (ap.get("exercise_results") or []):
        et = er.get("exercise_type")
        if et is not None:
            existing[et] = er

    mean_raw = ap.get("mean_grade", 0)
    try:
        mean_grade = float(mean_raw) if mean_raw not in (None, "") else 0.0
    except (TypeError, ValueError):
        mean_grade = 0.0

    return {
        "id": item.get("id"),
        "fullname": item.get("fullname", "") or "",
        "birth_date": item.get("birth_date"),
        "mean_grade": mean_grade,
        "aggregates": {
            "strength_score": ap.get("strength_score"),
            "speed_score": ap.get("speed_score"),
            "endurance_score": ap.get("endurance_score"),
            "physical_test_grade": ap.get("physical_test_grade"),
        },
        "existing_exercises": existing,
    }


def build_applicant_map(client: DalClient, campuses: list[str],
                        limit: int | None = None) -> dict:
    """Собрать normalized(name, dob) -> applicant record из API."""
    amap: dict[tuple[str, str], dict] = {}
    count = 0
    for campus in campuses:
        for item in client.list_applications(campus):
            rec = _applicant_record_from_api(item)
            key = core._key(rec["fullname"], rec["birth_date"])
            amap.setdefault(key, rec)
            count += 1
            if limit is not None and count >= limit:
                return amap
    return amap


def build_mock_applicant_map_from_fizo(fizo: core.FizoIndex,
                                       limit: int | None = None) -> dict:
    """Мок карты абитуриентов для --self-check (без HTTP)."""
    amap: dict[tuple[str, str], dict] = {}
    for i, rec in enumerate(fizo.records, start=1):
        key = core._key(rec["name"], rec["dob_raw"])
        if key in amap:
            continue
        amap[key] = {
            "id": 900000 + i,          # синтетический id
            "fullname": rec["name"],
            "birth_date": rec["dob"],  # dd.mm.yyyy — core нормализует одинаково
            "mean_grade": 0.0,
            "aggregates": {},
            "existing_exercises": {},
        }
        if limit is not None and len(amap) >= limit:
            break
    return amap


# ===========================================================================
# Построение плана (без HTTP)
# ===========================================================================
def _override_body_from_fill(fill: dict) -> dict:
    """Собрать тело запроса к ручке override из результата core.compute_fill."""
    results = [
        {
            "exercise_type": er["exercise_type"],
            "value": er["value_to_store"],
            "secondary_score": er["secondary_score"],
            "extra_params": er["extra_params"],
        }
        for er in fill["exercise_results"]
    ]
    return {
        "results": results,
        "strength_score": fill["strength_score"],
        "speed_score": fill["speed_score"],
        "endurance_score": fill["endurance_score"],
        "physical_test_grade": fill["physical_test_grade"],
    }


def build_plan(applicant_map: dict, fizo: core.FizoIndex, grades: core.GradeIndex,
               *, do_physical: bool, do_grade: bool) -> dict:
    """Собрать план намеченных действий для каждого совпавшего абитуриента."""
    plan = {
        "meta": {
            "scoring_mode": core.SCORING_MODE,
            "age_ref_date": core.AGE_REF_DATE.isoformat(),
            "do_physical": do_physical,
            "do_grade": do_grade,
            "applicants_in_map": len(applicant_map),
        },
        "physical_overrides": [],
        "grade_patches": [],
        "grade_conflicts": [],
        "unmatched_fizo": [],   # есть в ФИЗО, но нет абитуриента в карте
        "matched_no_data": [],  # абитуриент есть, но нет ни ФИЗО, ни грейда
    }

    matched_keys = set()

    for key, applicant in applicant_map.items():
        name = applicant["fullname"]
        dob = applicant["birth_date"]
        aid = applicant["id"]

        fill = core.compute_fill(name, dob, fizo, grades)
        touched = False

        # ---- физподготовка (ДОСЛОВНО через override) -------------------
        # Пропускаем тех, кто в ведомости есть, но не выполнил ни одного
        # упражнения (все нули) — заливать нечего, пустой override не нужен.
        if do_physical and fill["matched"] and fill["exercise_results"]:
            touched = True
            plan["physical_overrides"].append({
                "applicant_id": aid,
                "name": name,
                "dob": fill["dob"],
                "old": {
                    "aggregates": applicant.get("aggregates", {}),
                    "existing_exercise_types": sorted(
                        applicant.get("existing_exercises", {}).keys()
                    ),
                },
                "body": _override_body_from_fill(fill),
            })

        # ---- средний балл (fill-empty-plus-report-conflicts) -----------
        if do_grade and fill["mean_grade"] is not None:
            touched = True
            committee = float(fill["mean_grade"])
            db_grade = float(applicant.get("mean_grade") or 0.0)
            entry = {
                "applicant_id": aid,
                "name": name,
                "dob": fill["dob"],
                "db_mean_grade": db_grade,
                "committee_mean_grade": committee,
            }
            if db_grade <= 0:
                plan["grade_patches"].append({
                    **entry,
                    "old": db_grade,
                    "new": committee,
                    "body": {"mean_grade": committee},
                })
            elif abs(db_grade - committee) > 1e-9:
                plan["grade_conflicts"].append(entry)
            # else: совпало — ничего не делаем.

        if touched:
            matched_keys.add(key)
        elif fill["matched"] is False and fill["mean_grade"] is None:
            plan["matched_no_data"].append({
                "applicant_id": aid, "name": name, "dob": fill["dob"],
            })

    # ---- кто из ФИЗО не нашёл абитуриента в карте --------------------
    map_keys = list(applicant_map.keys())
    for rec in core.unmatched_fizo_report(fizo, [(k[0], k[1]) for k in map_keys]):
        plan["unmatched_fizo"].append({
            "name": rec["name"], "dob": rec["dob"], "row": rec["row"],
        })

    plan["counts"] = {
        "physical_overrides": len(plan["physical_overrides"]),
        "grade_patches": len(plan["grade_patches"]),
        "grade_conflicts": len(plan["grade_conflicts"]),
        "unmatched_fizo": len(plan["unmatched_fizo"]),
        "matched_no_data": len(plan["matched_no_data"]),
        "applicants_touched": len(matched_keys),
    }
    return plan


def write_plan(plan: dict) -> Path:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    PLAN_PATH.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    return PLAN_PATH


# ===========================================================================
# Исполнение плана против сервера (идемпотентно / resumable)
# ===========================================================================
def execute_plan(client: DalClient, plan: dict) -> dict:
    """Применить план. При execute=False клиент вернёт заглушки (dry-run)."""
    results = {"physical": [], "grade": []}

    for item in plan["physical_overrides"]:
        r = client.override_physical(item["applicant_id"], item["body"])
        results["physical"].append({
            "applicant_id": item["applicant_id"], "name": item["name"], "resp": r,
        })

    for item in plan["grade_patches"]:
        r = client.patch_application(item["applicant_id"], item["body"])
        results["grade"].append({
            "applicant_id": item["applicant_id"], "name": item["name"], "resp": r,
        })

    return results


# ===========================================================================
# CLI
# ===========================================================================
def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fill_prod.py",
        description=(
            "Вариант 2 (prod): дословная заливка ФИЗО (ручка override) и среднего "
            "балла в DAL API. По умолчанию DRY-RUN — без --execute сервер НЕ "
            "мутируется. Значения берутся из общего core.py."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--base-url", default=DEFAULT_BASE_URL,
                   help=f"Базовый URL DAL (по умолчанию {DEFAULT_BASE_URL}).")
    p.add_argument("--email", help="Email для получения JWT (или используйте --token).")
    p.add_argument("--password", help="Пароль для получения JWT.")
    p.add_argument("--token", help="Готовый Bearer JWT (в обход email/password).")

    grp = p.add_mutually_exclusive_group()
    grp.add_argument("--dry-run", dest="dry_run", action="store_true", default=True,
                     help="Ничего не мутировать (по умолчанию включено).")
    grp.add_argument("--execute", dest="dry_run", action="store_false",
                     help="РЕАЛЬНО писать в сервер (ручной шаг пользователя).")

    p.add_argument("--limit", type=int, default=None,
                   help="Ограничить число обрабатываемых абитуриентов.")

    only = p.add_mutually_exclusive_group()
    only.add_argument("--only-physical", action="store_true",
                      help="Только физподготовка (без среднего балла).")
    only.add_argument("--only-grade", action="store_true",
                      help="Только средний балл (без физподготовки).")

    p.add_argument("--campus", action="append", default=None,
                   help=("Код(ы) кампуса для листинга (можно повторять). "
                         f"По умолчанию {PHYSICAL_CAMPUSES}."))

    p.add_argument("--self-check", action="store_true",
                   help=("Собрать план из xlsx БЕЗ HTTP: карта абитуриентов "
                         "мокается из имён ФИЗО. Печатает counts и пишет plan.json."))
    return p


def _print_counts(plan: dict, header: str) -> None:
    print(header)
    c = plan["counts"]
    print(f"  applicants_in_map  : {plan['meta']['applicants_in_map']}")
    print(f"  applicants_touched : {c['applicants_touched']}")
    print(f"  physical_overrides : {c['physical_overrides']}")
    print(f"  grade_patches      : {c['grade_patches']}")
    print(f"  grade_conflicts    : {c['grade_conflicts']}")
    print(f"  unmatched_fizo     : {c['unmatched_fizo']}")
    print(f"  matched_no_data    : {c['matched_no_data']}")


def main(argv=None) -> int:
    args = _build_arg_parser().parse_args(argv)

    do_physical = not args.only_grade
    do_grade = not args.only_physical
    campuses = args.campus or PHYSICAL_CAMPUSES

    fizo = core.load_fizo()
    grades = core.load_grades()

    # ------------------------------------------------------------------
    # SELF-CHECK: без HTTP, карта мокается из ФИЗО.
    # ------------------------------------------------------------------
    if args.self_check:
        print("=== SELF-CHECK (no HTTP) ===")
        print(f"core.SCORING_MODE = {core.SCORING_MODE!r}")
        print(f"ФИЗО records loaded : {len(fizo.records)}")
        print(f"grade records loaded: {len(grades.records)}")

        amap = build_mock_applicant_map_from_fizo(fizo, limit=args.limit)
        print(f"mock applicant map  : {len(amap)} (unique name+dob from ФИЗО)")

        plan = build_plan(
            amap, fizo, grades, do_physical=do_physical, do_grade=do_grade
        )
        path = write_plan(plan)
        _print_counts(plan, "PLAN counts:")
        print(f"plan.json written to: {path}")

        sample = {
            "physical_overrides_sample": plan["physical_overrides"][:2],
            "grade_patches_sample": plan["grade_patches"][:2],
        }
        print("sample:")
        print(json.dumps(sample, ensure_ascii=False, indent=2, default=str))
        print("SELF-CHECK OK: план собран без обращения к серверу.")
        return 0

    # ------------------------------------------------------------------
    # Реальный режим (dry-run по умолчанию): требуется соединение.
    # ------------------------------------------------------------------
    execute = not args.dry_run
    client = DalClient(args.base_url, token=args.token, execute=execute)

    if not args.token:
        if not (args.email and args.password):
            print("ERROR: нужен --token ИЛИ --email + --password (или --self-check).",
                  file=sys.stderr)
            return 2
        client.obtain_token(args.email, args.password)

    print(f"=== {'EXECUTE (MUTATING)' if execute else 'DRY-RUN (read-only)'} ===")
    print(f"base_url = {args.base_url}  campuses = {campuses}")

    applicant_map = build_applicant_map(client, campuses, limit=args.limit)
    print(f"applicants fetched: {len(applicant_map)}")

    plan = build_plan(
        applicant_map, fizo, grades, do_physical=do_physical, do_grade=do_grade
    )
    path = write_plan(plan)
    _print_counts(plan, "PLAN counts:")
    print(f"plan.json written to: {path}")

    if not execute:
        print("\nDRY-RUN: сервер НЕ изменён. Полный план — в plan.json.")
        print("Чтобы применить, перезапустите с --execute (ручной шаг пользователя).")
        return 0

    print("\nEXECUTE: применяю план...")
    results = execute_plan(client, plan)
    print(f"physical ops: {len(results['physical'])}  grade ops: {len(results['grade'])}")
    print("DONE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
