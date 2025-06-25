import pandas as pd
import json
import argparse

# Map pandas dtypes to Personalize schema types
dtype_mapping = {
    "object": "string",
    "int64": "int",
    "float64": "float",
    "bool": "boolean"
}

def generate_schema(csv_path, schema_name="Schema", dataset_type="Interactions", namespace="com.amazonaws.personalize.schema"):
    df = pd.read_csv(csv_path)

    fields = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        p_type = dtype_mapping.get(dtype, "string")  # default to string if unknown
        fields.append({ "name": col, "type": p_type })

    schema = {
        "type": "record",
        "name": schema_name,
        "namespace": namespace,
        "fields": fields,
        "version": "1.0"
    }

    output_filename = f"{dataset_type.lower()}_schema.json"
    with open(output_filename, "w") as f:
        json.dump(schema, f, indent=4)

    print(f"✅ Schema for {dataset_type} saved to '{output_filename}'")

# Command-line usage: python generate_schema.py --csv interactions.csv --type Interactions
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to input CSV file")
    parser.add_argument("--name", default="Schema", help="Schema name")
    parser.add_argument("--type", choices=["Interactions", "Users", "Items"], default="Interactions", help="Dataset type")
    args = parser.parse_args()

    generate_schema(args.csv, schema_name=args.name, dataset_type=args.type)
