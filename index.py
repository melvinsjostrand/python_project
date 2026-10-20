import os
import matplotlib.pyplot as plt
from datetime import datetime


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

    file = open(filename, "r", encoding="utf-8")
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
        word_count(line,stats["word_counts"])
    
    file.close()
    stats["avg_wpl"] = stats["words"] / stats["lines"] if stats["lines"] > 0 else 0
    stats["avg_cpw"] = stats["chars"] / stats["words"] if stats["words"] > 0 else 0
    return stats


def word_count(line,word_count):

    line = line.lower().split()

    for word in line:
        word = word.strip(".,!?;:”’()-_")
        if word:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
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


def save_section(results, filename, section, data):
    if filename not in results:
        results[filename] = {}
    results[filename][section] = data
    return results

def export_pdf(results,filename):
    if not results:
        print("Nothing to export. Run option 2-5 first.")
        return
    os.makedirs("results", exist_ok=True)
    name = filename.replace(".txt", "")
    path = os.path.join("results", f"{name}_results.txt")
    print(results)
    file = open(path, "w", encoding="utf-8")
    for filename, sections in results.items():
        file.write("=" * 60 + "\n")
        file.write("TEXT ANALYSIS RESULTS\n")
        file.write("=" * 60 + "\n")
        file.write(f"File analysed: {filename}\n")
        file.write(f"Analysis date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n")

        for section, data in sections.items():
            file.write(section.upper() + "\n")
            file.write("-" * 30 + "\n")
            for key, value in data.items():
                file.write(f"{key}: {value}\n")
            file.write("\n")

    file.write("=" * 60 + "\n")
    file.write("End of Analysis Report\n")
    file.write("=" * 60 + "\n")
    file.close()

    print(f"Results exported to {path}")

    
def main():
    menu = '''
==================================================
 TEXT ANALYSER
==================================================
1. Load text file
2. Display basic statistics
3. Word frequency analysis
4. Sentence analysis
5. Character analysis
6. Export results
7. Exit
==================================================
'''

    running = True
    stats = None
    filename = None
    results = {}
    while running == True:
        print(menu)
        if filename != None:
            print("Current file: ", filename)
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
                if filename is not None:
                    stats = file_reader(filename)
                    results = {}
            case 2 | 3 | 4 | 5 | 6 if filename is None:
                print("No file is loaded. Pick 1 to load a file")
            case 2:
                print("Total number of lines: ",stats["lines"])
                print("Total number of words: ",stats["words"])
                print("Total number of characters without spaces",stats["chars"])
                print("Total number of characters with spaces", stats["chars_with_spaces"])
                print("Average words per line:", round(stats["avg_wpl"]))
                print("Average characters per word: ",round(stats["avg_cpw"]))
                results = save_section(results, filename, "Basic statistics", {
                "Lines": stats["lines"],
                "Words": stats["words"],
                "Characters": stats["chars"],
                "Characters with spaces": stats["chars_with_spaces"],
                "Average words per line": round(stats["avg_wpl"], 1),
                "Average characters per word": round(stats["avg_cpw"], 1)
            })
                input("Press Enter to open graph...")
                vis_graph(filename, stats["lines"],stats["words"],stats["chars"],stats["chars_with_spaces"],stats["avg_wpl"],stats["avg_cpw"])

                input("Press Enter to continue...")
            case 3:
                appear_once = 0
                items = [(count, word) for word, count in stats["word_counts"].items()]
                items.sort(reverse=True)
                total = stats["words"]
                letter_words = [word for word in stats["word_counts"] if word.isalpha()]
                longest = max(letter_words, key=len)
                shortest = min(letter_words, key=len)

                print(f"Longest word: {longest} ({len(longest)} characters)")
                print(f"Shortest word: {shortest} ({len(shortest)} characters)")
                print("Top 10 most common words:")
                for place, (count, word) in enumerate(items[:10], start=1):
                    percent = count / total * 100
                    print(f"{place:>2}. {word:<12} {count:>7,} times ({percent:>4.1f}%)")

                print(len(stats["word_counts"]))
                for count, word in items:
                    if count == 1:
                        appear_once += 1

                print(appear_once)
                word_data = {
                    "Unique words": len(stats["word_counts"]),
                    "Words appearing only once": appear_once
                }
                for place, (count, word) in enumerate(items[:10], start=1):
                    percent = count / total * 100
                    word_data[f"{place:>2}. {word:<12}"] = f"{count:>7,} times ({percent:>4.1f}%)"

                results = save_section(results, filename, "Word analysis", word_data)
                
                print("Saved sections:", list(results[filename].keys()))
                input("Press Enter to continue...")
            case 4:
                print("4")
                input("Press Enter to continue...")
            case 5:
                print("5")
                input("Press Enter to continue...")
            case 6:
                export_pdf(results,filename)
            case 7:
                print("Thank you for using Text Analyser!")
                running = False
            case _:
                print("invalid choice: pick between 1-7")



main()