"""Script to import military offices from Excel file."""
import pandas as pd
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from common.models.military import MilitaryOffice


def import_military_offices(excel_file_path):
    """Import military offices from Excel file."""
    print(f"Reading data from {excel_file_path}")
    
    # Read Excel file
    df = pd.read_excel(excel_file_path)
    
    # Assuming Excel has columns: name, city, code
    count = 0
    for _, row in df.iterrows():
        name = row.get('name')
        if not name:
            continue
            
        city = row.get('city', '')
        code = row.get('code', '')
        
        # Create or update military office
        office, created = MilitaryOffice.objects.update_or_create(
            name=name,
            defaults={
                'city': city,
                'code': code,
                'is_custom': False
            }
        )
        
        if created:
            print(f"Created military office: {name}")
        else:
            print(f"Updated military office: {name}")
        
        count += 1
    
    print(f"Successfully imported {count} military offices")


if __name__ == "__main__":
    # Change this to the path of your Excel file
    excel_file = "path/to/your/military_offices.xlsx"
    import_military_offices(excel_file)
