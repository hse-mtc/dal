"""Скрипт для получения публичных ссылок на все папки кампусов."""

import sys
from pathlib import Path

# Добавляем src в path для импортов
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.disk import DiskService
from src.campuses import Campus
from src.service import CAMPUSES_FOLDER


def main():
    ds = DiskService(token='token')

    print("Публичные ссылки на папки кампусов:\n")
    print("=" * 60)

    for abbr, campus_name in Campus.choices():
        campus_folder_path = CAMPUSES_FOLDER / campus_name

        public_url = ds.read_share_folder_with_anyone(campus_folder_path)
        
        print(f"\n{campus_name} ({abbr}):")
        print(f"  {public_url}")

    print("\n" + "=" * 60)
    print("Откройте ссылки в браузере для доступа к документам.")


if __name__ == "__main__":
    main()
