import os
import pandas as pd

vav_folder = '../HVAC_NewData/'
output_path = '../outputs/connection_mapping_analysis/VAV_Field_Availability.csv'

vav_files = sorted([f for f in os.listdir(vav_folder) if f.endswith('.csv') and not f.startswith('RTU') and f != 'README.csv'])


all_fields = set()
field_dict = {}

for file in vav_files:
    df = pd.read_csv(os.path.join(vav_folder, file), nrows=1)
    fields = set(df.columns)
    field_dict[file] = fields
    all_fields.update(fields)


all_fields = sorted(list(all_fields))


availability = pd.DataFrame(index=all_fields, columns=vav_files)

for file in vav_files:
    for field in all_fields:
        availability.at[field, file] = '✅' if field in field_dict[file] else '❌'

availability.to_csv(output_path)
print(f"[Saved] Clean field matrix saved to: {output_path}")
