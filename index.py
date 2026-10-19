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
def file_reader(filename):
    stats = {
    "lines": 0,
    "words": 0,
    "chars": 0,
    "chars_with_spaces": 0,
    "word_counts": {}
    }

    file = open(filename, 'r', encoding="utf-8")
    #går igenom hela filen rad för rad
    for line in file:
        #lägger ihop alla ord
        stats["words"] += words(line)
        #lägger ihop alla karaktärer med spaces jag hämtar
        stats["chars_with_spaces"] += chars_with_space(line)
        #lägger ihop alla karaktärer utan spaces jag hämtar 
        stats["chars"] += chars(line)
        #räknar antal rader
        stats["lines"] += 1
    
    file.close()
    stats["avg_wpl"] = stats["words"] / stats["lines"] if stats["lines"] > 0 else 0
    stats["avg_cpw"] = stats["chars"] / stats["words"] if stats["words"] > 0 else 0
    return stats

#hämtar alla ord jag har på en line       
def words(line):
    return len(line.split())

def chars_with_space(line):
    count = 0
    for ch in line:
        count += 1
    return count

#Hämtar alla karaktärer på raden
def chars(line):
    count = 0
    line = line.rstrip("\n").replace(" ", "")
    for ch in line:
        count += 1
    return count


#Skapar grafen för basic stats
def vis_graph(filename, lines, words, characters,characters_with_spaces,avg_wpl, avg_cpw):
    #delar upp grafen i två delar så att man kan se de olika värdena
    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Basic statistics for:" + filename, fontweight="bold")    
    plt.ylabel("Count")
    #Gör min vänsta och högra graf. väljer färg.
    right.bar(["Words per line", "Characters per word"], [avg_wpl, avg_cpw],
          color=["gold", "plum"])
    left.bar(["Lines", "Words", "Characters", "Characters with spaces"], [lines, words, characters, characters_with_spaces],
         color=["skyblue", "lightgreen", "lightcoral", "purple"])

    plt.tight_layout()
    plt.show()


#sparar alla resultat i ett set
def save_result(results, filename, lines,words,chars,chars_with_spaces,avg_wpl, avg_cpw):
    for saved in results:
        #kollar ifall settet redan finns sparat
        if saved[1] == filename:
            print(f"{filename} is already saved")
            return results
    new_id = len(results) + 1
    file_type = filename.split(".")[-1]
    results.add((new_id, filename, file_type, lines, words, chars, chars_with_spaces,avg_wpl, avg_cpw))
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
    stats = None
    filename = None
    results = set()
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
                if file is not None:
                    stats = file_reader(filename)

                print(stats)
            case 2 | 3 | 4 | 5 | 6 if filename is None:
                print("No file is loaded. Pick 1 to load a file")
            case 2:
                print("Total number of lines: ",stats["lines"])
                print("Total number of words: ",stats["words"])
                print("Total number of characters without spaces",stats["chars"])
                print("Total number of characters with spaces", stats["chars_with_spaces"])
                print("Average words per line:", round(stats["avg_wpl"]))
                print("Average characters per word: ",round(stats["avg_cpw"]))
                vis_graph(filename, stats["lines"],stats["words"],stats["chars"],stats["chars_with_spaces"],stats["avg_wpl"],stats["avg_cpw"])
                results = save_result(results, filename, stats["lines"], stats["words"],stats["chars"], stats["chars_with_spaces"],round(stats["avg_wpl"]), round(stats["avg_cpw"]))
                print(results)
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