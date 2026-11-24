import os
import re
import collections
import time
import tempfile

class FileManipulator:
    def __init__(self, file_path):
        self.file_path = file_path

    def run_cli(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                pass
        except FileNotFoundError or PermissionError:
            print("FILE NOT FOUND. PLEASE CHECK THE FILE PATH.")
            return
        while True:
            print("\nOPTIONS:")
            print("1. Show basic statistics")
            print("2. Show most repeated words")
            print("3. Replace a word in the file")
            print("4. Exit")
            time.sleep(1)
            choice = input("ENTER YOUR CHOICE (1-4): ").strip()
            
            if choice == "1":
                stats = self.basic_stats()
                print(stats)
                time.sleep(5)
            elif choice == "2":
                content = self.read_file()
                top_n = self.top_n_words()
                self.most_repeated_words(content, top_n)
                time.sleep(5)
            elif choice == "3":
                result = self.run_manipulation()
                print(result)
                time.sleep(5)
            elif choice == "4":
                print("EXITING...")
                break
            else:
                print("INVALID CHOICE. PLEASE ENTER A NUMBER BETWEEN 1 AND 4.")
                time.sleep(1)
    
    
    def read_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = list()
            for line in file:
                content.append(line)
            return "".join(content)

    def basic_stats(self):
        empty_lines_count = 0
        words = 0        
        try:
            content = self.read_file()
            lines = content.splitlines()
            total_lines_count = len(lines)
            for line in lines:
                if line.strip() == "":
                    empty_lines_count += 1
                words += len(line.split())
            
            return f"Total lines: {total_lines_count} | Empty lines: {empty_lines_count} | Words: {words}"
        except FileNotFoundError:
            return "FILE NOT FOUND"

    def top_n_words(self):
        while True:
            try:
                question = int(input("ENTER THE NUMBER OF TOP REPEATED WORDS YOU WANT TO SEE: "))
                if question > 0:
                    return question
                else:
                    print("PLEASE ENTER A POSITIVE INTEGER.")
            except ValueError:
                print("INVALID INPUT. PLEASE ENTER A POSITIVE INTEGER.")


    def most_repeated_words(self, content, top_n):
        if not content:
            return "FILE IS EMPTY"
        turkish_text = content.translate(str.maketrans({
            "İ": "i",
            "I": "ı"
        })).lower()        
        words = re.findall(r'\b\w+\b', turkish_text)
        word_count = collections.Counter(words)
        if not word_count:
            return "NO WORDS FOUND"
        
        top_n = min(top_n, len(word_count))        
        commons = word_count.most_common(top_n)
        max_word_len = max(len(word) for word, _ in commons) + 2
        max_count_len = max(len(str(count)) for _, count in commons)
        print("-" * (max_word_len + max_count_len + 6))
        for word, count in commons:
            print(f"{word:<{max_word_len}} | {count:>{max_count_len}}")
        print("-" * (max_word_len + max_count_len + 6))

    
    def safe_write_file(self, content):
        target = self.file_path
        temp_path = None
        try:        
            with tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=False, dir=os.path.dirname(target) or ".", suffix= ".tmp") as temp_file:
                temp_path = temp_file.name
                temp_file.write(content)
                temp_file.flush()
                os.fsync(temp_file.fileno())
            os.replace(temp_path, target)
        except OSError as e:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    print(f"ERROR REMOVING TEMP FILE: {temp_path}")
            return f"ERROR WRITING TO FILE: {e}"
        return "FILE WRITTEN SUCCESSFULLY"
        
    def input_user_to_manipulate(self):
        while True:
            old_word = input("ENTER THE WORD YOU WANT TO REPLACE: ").strip()
            new_word = input("ENTER THE NEW WORD: ").strip()
            if old_word and new_word:
                return old_word, new_word
            print("INVALID INPUT. PLEASE ENTER NON-EMPTY STRINGS.")

    def run_manipulation(self):
        try:
            old_content = self.read_file()

        except FileNotFoundError:
            return "FILE NOT FOUND"    

        new_content, count = self.manipulate_file(old_content, *self.input_user_to_manipulate())
        if count == 0:
            return "NO MATCHES FOUND"

        while True: 
            question = input(f"{count} MATCHES FOUND. DO YOU WANT TO SAVE THE CHANGES? (Y/N): ").strip().lower()        
            if question == "y":
                write_status = self.safe_write_file(new_content)
                return write_status
            elif question == "n":
                return "CHANGES NOT SAVED"
            print("INVALID INPUT. PLEASE ENTER 'Y' OR 'N'.")

    def manipulate_file(self, old_content, old_word, new_word):
        if old_word == "" or new_word == "":
            return old_content, 0
        sanitized_word = re.escape(old_word)
        new_content, count = re.subn(rf'(?<!\w){sanitized_word}(?!\w)', new_word, old_content, flags=re.IGNORECASE)
        return new_content, count

if __name__ == "__main__":
    processor = FileManipulator("test1.txt")
    processor.run_cli()