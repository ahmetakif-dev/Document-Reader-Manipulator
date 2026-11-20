import re
class FileManipulator:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = list()
                for line in file:
                    keep = line.strip()
                    if keep != "":
                        content.append(keep.lower())
                return "\n".join(content)

        except FileNotFoundError:
            return "FILE NOT FOUND"
        
        except Exception as e:
            return f"AN ERROR OCCURRED"

    def input_user_to_manipulate(self):
        while True:
            old_word = input("ENTER THE WORD YOU WANT TO REPLACE: ").strip()
            new_word = input("ENTER THE NEW WORD: ").strip()
            if old_word and new_word:
                return old_word, new_word
            print("INVALID INPUT. PLEASE ENTER NON-EMPTY STRINGS.")

    def run_manipulation(self):
        old_content = self.read_file()
        if old_content == "FILE NOT FOUND" or old_content == "AN ERROR OCCURRED":
            return old_content

        new_content, count = self.manipulate_file(old_content, *self.input_user_to_manipulate())
        if count == 0:
            return "NO MATCHES FOUND"

        else:
            while True: 
                question = input(f"{count} MATCHES FOUND. DO YOU WANT TO SAVE THE CHANGES? (Y/N): ").strip().lower()        
                if question == "y":
                    return new_content
                elif question == "n":
                    return old_content
                else:
                    print("INVALID INPUT. PLEASE ENTER 'Y' OR 'N'.")
            
    def manipulate_file(self, old_content, old_word, new_word):
        if old_word == "" or new_word == "":
            return old_content, 0
        sanitized_word = re.escape(old_word)
        new_content, count = re.subn(rf'(?<!\w){sanitized_word}(?!\w)', new_word, old_content, flags=re.IGNORECASE)
        return new_content, count

print(FileManipulator("test1.txt").run_manipulation())