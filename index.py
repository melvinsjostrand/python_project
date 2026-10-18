import os
#För att hämta alla mina txt filer som jag har nersparat
def get_files():
    txt_files = []
    print(os.getcwd())
    for name in os.listdir("."):
        if name.lower().endswith(".txt"):
            txt_files.append(name)
    return txt_files


#för att välja vilken fil du vill läsa
def load_file(files):  
    choice = input(f"Type the filename you want to read or choose a file between 1 - {len(files)}: ")
    if choice.isdigit() and 1 <= int(choice) <= len(files):
        filename = files[int(choice) - 1]
        print(filename)
        return filename
    if choice + ".txt" in files:
        print(f"Loading {choice}")
        return choice + ".txt"
    print("File not found. Pick 1 to try again")
    return None


#för att läsa och räkna grundstatistik
def basic_statistics(filename):
    total_words = 0
    file = open(filename, 'r', encoding="utf-8")
    for line in file:
        total_words += words(line)

    return "no", total_words, "no"


def words(line):
    return len(line.split())



def main():
    menu = '''
    Welcome to our program. choose what u wanna do (1-7)
    (1) Load a text file
    (2) Display basic statistics
    (3) Show word frequency analysis 
    (4) Display sentence analysis
    (5) Display character analysis
    (6) Export results
    (7) Exit programme
    '''

    print(menu)
    running = True
    filename = None
    while running == True:
        print()
        answer = input("choose what u wanna do (1-7)")
        if not answer.isdigit():
            print("Invalid choice: Pick between 1-7")
            continue
        choice = int(answer)
        match choice:
            case 1:
                files = get_files()
                print("files available: ")
                for file in range(len(files)):
                    print(file + 1,files[file])
                filename = load_file(files)
            case 2 | 3 | 4 | 5 | 6 if filename is None:
                print("No file is loaded. Pick 1 to load a file")
            case 2:
                lines, words, characters = basic_statistics(filename)
                print(lines)
                print(words)
                print(characters)
            case 3:
                print("3")
            case 4:
                print("4")
            case 5:
                print("5")
            case 6:
                print("6")
            case 7:
                print("7")
                running = False
            case _:
                print("invalid choice: pick between 1-7")



main()