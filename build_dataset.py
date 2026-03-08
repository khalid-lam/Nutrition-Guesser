import pandas as pd
from PIL import Image
import os

def parse_dish_line(line):
    parts = [p.strip() for p in line.split(',')]
    dish_id = parts[0]
    total_calories = float(parts[1])
    total_mass = float(parts[2])
    total_fat = float(parts[3])
    total_carb = float(parts[4])
    total_protein = float(parts[5])
    ingredients = []
    for i in range(6, len(parts), 7):
        if i + 6 < len(parts):
            ingr_id = parts[i]
            name = parts[i+1]
            mass = float(parts[i+2])
            cal = float(parts[i+3])
            fat = float(parts[i+4])
            carb = float(parts[i+5])
            prot = float(parts[i+6])
            ingredients.append(name.strip())
    return {
        'dish_id': dish_id,
        'total_calories': total_calories,
        'total_mass': total_mass,
        'total_fat': total_fat,
        'total_carb': total_carb,
        'total_protein': total_protein,
        'ingredients': ', '.join(ingredients)
    }

# Load data from both CSVs
data = []
for csv_file in ['data/dishes_metadata/dish_metadata_cafe1.csv', 'data/dishes_metadata/dish_metadata_cafe2.csv']:
    with open(csv_file, 'r') as f:
        for line in f:
            if line.strip():
                dish = parse_dish_line(line)
                data.append(dish)

df = pd.DataFrame(data)

# Ensure dish_id is string
df['dish_id'] = df['dish_id'].astype(str)

# Load all dish IDs
with open('data/dishes_metadata/dish_ids_all.txt', 'r') as f:
    all_dish_ids = [line.strip() for line in f]

# Filter to only those with images
dish_ids = [dish_id for dish_id in all_dish_ids if os.path.exists(f'data/overhead/{dish_id}/rgb.png')]

# Filter df to matching dish_ids
df = df[df['dish_id'].isin(dish_ids)]

# Add image paths
df['rgb_image_path'] = [f'data/overhead/{dish_id}/rgb.png' for dish_id in df['dish_id']]

# Save the dataset
df.to_pickle('dish_dataset.pkl')

print("Dataset created and saved as dish_dataset.pkl")
print(f"Shape: {df.shape}")
print(f"Sample ingredients for first dish: {df['ingredients'].iloc[0] if len(df) > 0 else 'No data'}")