import os
import json

def count_jsonl_entries(root_dir):
    """
    Count the number of entries in JSONL files within a directory structure.
    
    Args:
        root_dir (str): The root directory to search for JSONL files (e.g., 'data_gpt_4' or 'data_gpt_3_5')
    
    Returns:
        int: Total files processed
    """
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        print(f"Error: '{root_dir}' directory not found!")
        return 0
    
    # Get all subdirectories in the root directory
    subdirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
    
    # Track total files processed and entry statistics
    total_files = 0
    total_entries = 0
    min_entries = float('inf')
    max_entries = 0
    
    print(f"\nExamining JSONL files in {root_dir}/...")
    print("-" * 70)
    
    # Iterate through each subdirectory
    for subdir in sorted(subdirs):
        subdir_path = os.path.join(root_dir, subdir)
        print(f"\nIn directory: {subdir_path}")
        
        # Get all JSONL files in the current subdirectory
        jsonl_files = [f for f in os.listdir(subdir_path) if f.endswith('.jsonl')]
        
        if not jsonl_files:
            print("  No JSONL files found in this directory.")
            continue
        
        # Iterate through each JSONL file
        for jsonl_file in sorted(jsonl_files):
            file_path = os.path.join(subdir_path, jsonl_file)
            entries = 0
            
            try:
                # Count lines in the JSONL file (each line is a JSON object)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():  # Skip empty lines
                            try:
                                json.loads(line)  # Try to parse the JSON to ensure it's valid
                                entries += 1
                            except json.JSONDecodeError:
                                pass  # Skip invalid JSON lines
                
                print(f"  {jsonl_file}: {entries} entries")
                
                # Update statistics
                total_entries += entries
                min_entries = min(min_entries, entries)
                max_entries = max(max_entries, entries)
                total_files += 1
                
            except Exception as e:
                print(f"  Error reading {jsonl_file}: {str(e)}")
    
    # Print summary statistics
    if total_files > 0:
        print("\n" + "-" * 70)
        print(f"Summary for {root_dir}:")
        print(f"  Total JSONL files: {total_files}")
        print(f"  Total entries: {total_entries}")
        print(f"  Average entries per file: {total_entries / total_files:.2f}")
        print(f"  Minimum entries in a file: {min_entries}")
        print(f"  Maximum entries in a file: {max_entries}")
    
    return total_files

def main():
    """Main function to count entries in JSONL files in both directories."""
    print("JSONL Entry Counter")
    print("=" * 70)
    
    # Count entries in data_gpt_3_5
    files_3_5 = count_jsonl_entries('data_gpt_3_5')
    
    # Count entries in data_gpt_4
    files_4 = count_jsonl_entries('data_gpt_4')
    
    # Print overall summary
    print("\n" + "=" * 70)
    print(f"Overall Summary:")
    print(f"  Total JSONL files processed: {files_3_5 + files_4}")
    print("=" * 70)

if __name__ == "__main__":
    main() 