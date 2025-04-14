import os
import json

def count_arrays_in_json_files():
    """
    Traverse through the datasets directory and all its subdirectories,
    read each JSON file, and print the length of the array inside each file.
    """
    # Path to the datasets directory
    datasets_dir = 'datasets'
    
    # Check if the datasets directory exists
    if not os.path.exists(datasets_dir):
        print(f"Error: '{datasets_dir}' directory not found!")
        return
    
    # Get all subdirectories in the datasets directory
    subdirs = [d for d in os.listdir(datasets_dir) if os.path.isdir(os.path.join(datasets_dir, d))]
    
    # Track total number of files processed
    total_files = 0
    
    print(f"Examining JSON files in {datasets_dir}/...")
    print("-" * 60)
    
    # Iterate through each subdirectory
    for subdir in sorted(subdirs):
        subdir_path = os.path.join(datasets_dir, subdir)
        print(f"\nIn directory: {subdir_path}")
        
        # Get all JSON files in the current subdirectory
        json_files = [f for f in os.listdir(subdir_path) if f.endswith('.json')]
        
        if not json_files:
            print("  No JSON files found in this directory.")
            continue
        
        # Iterate through each JSON file
        for json_file in sorted(json_files):
            file_path = os.path.join(subdir_path, json_file)
            
            try:
                # Read the JSON file
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check if the content is an array
                if isinstance(data, list):
                    array_length = len(data)
                    print(f"  {json_file}: {array_length} items")
                else:
                    print(f"  {json_file}: Not an array (type: {type(data).__name__})")
                
                total_files += 1
                
            except json.JSONDecodeError as e:
                print(f"  Error parsing {json_file}: {str(e)}")
            except Exception as e:
                print(f"  Error reading {json_file}: {str(e)}")
    
    print("\n" + "-" * 60)
    print(f"Total JSON files processed: {total_files}")

if __name__ == "__main__":
    count_arrays_in_json_files() 