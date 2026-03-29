import os

def count_all_python_words(start_dir=r"C:\uni_year_3\dissertation\application\TASK-backend"):
    total_words = 0
    file_count = 0
    
    # os.walk goes through the current folder AND all subfolders
    for root, dirs, files in os.walk(start_dir):
        # Optional: Skip hidden folders like .git or environments
        if any(skip in root for skip in ['.git', 'venv', '__pycache__']):
            continue

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # .split() handles spaces, tabs, and newlines
                        word_list = f.read().split()
                        count = len(word_list)
                        total_words += count
                        file_count += 1
                        
                        # Show the path so you know where the file is
                        print(f"{file_path:<50} | {count} words")
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")

    print("-" * 65)
    print(f"Grand Total: {total_words} words across {file_count} .py files.")

if __name__ == "__main__":
    count_all_python_words()