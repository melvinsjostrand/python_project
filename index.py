import os
import matplotlib.pyplot as plt

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
    amount_char = 0
    lines = 0
    file = open(filename, 'r', encoding="utf-8")
    for line in file:
        total_words += words(line)
        amount_char += chars(line)
        lines += 1

    avg_wpl = total_words / lines
    avg_cpw = amount_char / total_words
    return lines, total_words, amount_char, avg_wpl,avg_cpw 

def chars(line):
    count = 0
    line = line.rstrip("\n").replace(" ", "")
    for ch in line:
        count += 1
    return count

        
def words(line):
    return len(line.split())


def vis_graph(filename, lines, words, characters,avg_wpl, avg_cpw):

    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Basic statistics for:" + filename, fontweight="bold")    
    plt.ylabel("Count")
    right.bar(["Words per line", "Characters per word"], [avg_wpl, avg_cpw],
          color=["gold", "plum"])
    left.bar(["Lines", "Words", "Characters"], [lines, words, characters],
         color=["skyblue", "lightgreen", "lightcoral"])

    plt.tight_layout()
    plt.show()

def save_result(results, filename, lines,words,chars, avg_wpl, avg_cpw):
    for saved in results:
        if saved[1] == filename:
            print(f"{filename} is already saved")
            return results
    new_id = len(results) + 1
    file_type = filename.split(".")[-1]
    results.add((new_id, filename, file_type, lines, words, chars, avg_wpl, avg_cpw))
    return results

    
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
    result = set()
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
                lines, words, characters,avg_wpl, avg_cpw = basic_statistics(filename)
                avg_cpw = round(avg_cpw)
                avg_wpl = round(avg_wpl)
                print(avg_cpw, avg_wpl)
                vis_graph(filename, lines, words, characters,avg_wpl, avg_cpw)
                result = save_result(result, filename, lines, words, characters, avg_wpl, avg_cpw)

                print(result)




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