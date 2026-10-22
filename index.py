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
    "word_counts": {},
    "letter_counter":{},
    "sentence": [],
    "digits": 0
    }
    current = "" #buffert till sentence funktionen


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
        #Räknar antalet olika ord det finns i en text.
        word_count(line,stats["word_counts"])
        #sparar i bufferten
        current = sentence(line, current, stats["sentence"])
<<<<<<< Updated upstream
        amount_letters(line,stats["letter_counter"])
=======
        most_common_letter(line,stats["letter_counter"])
        stats["digits"] += digits(line)
>>>>>>> Stashed changes
    #Det som blev över när filen tog slut.
    if current.strip():
        stats["sentence"].append(current.strip())
    
    file.close()
    stats["avg_wpl"] = stats["words"] / stats["lines"] if stats["lines"] > 0 else 0
    stats["avg_cpw"] = stats["chars"] / stats["words"] if stats["words"] > 0 else 0
    return stats

#Går igenom en "line" och kollar när det finns ett slut
def sentence(line, current, sentences):
    line = line.strip()
    for i in range(len(line)):
        current += line[i]
        if line[i] in ".!?": #Letar efter skilljetecken
            if i + 1 == len(line) or line[i+1] == " ":# kollar om en mening verkligen är slut. 
                sentences.append(current.strip())
                current=""
    current += " "#lägger till space efter den har gått igenom en "line"
    return current

#Går igenom linjer och räknar hur många av varje ord som finns.
def word_count(line,word_count):
    line = line.lower().split()
    for word in line:
        word = word.strip(".,!?;:”’()-_'\"")
        if word:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

#hämtar alla ord jag har på en line       
def words(line):
    return len(line.split())

def chars_with_space(line):
    return len(line.rstrip("\n"))

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

#sparar all data i blocket, kollar också filnamn och ifall resultat har någon data i sig
def save_section(results, filename, section, data):
    #kollar ifall filen inte finns i resultat. om den inte finns så rensar jag mitt resultat
    if filename not in results:
        results[filename] = {}
    results[filename][section] = data
    return results

def export_txt(results,filename):
    #Kollar ifall resultat har någon data i sig
    if not results:
        print("Nothing to export. Run option 2-5 first.")
        return
    #Skapar en mapp och om den redan finns så skippar den att skapa
    os.makedirs("results", exist_ok=True)
    #Gör om namnet så det inte finns ".txt" i sig
    name = filename.replace(".txt", "")
    #Hämtar pathen till mappen och sen får du namnet "Filnamn" + resultat
    path = os.path.join("results", f"{name}_results.txt")
    print(results)
    file = open(path, "w", encoding="utf-8")
    #Delar upp så jag kan hantera mina "sections"
    for filename, sections in results.items():
        file.write("=" * 60 + "\n")
        file.write("TEXT ANALYSIS RESULTS\n")
        file.write("=" * 60 + "\n")
        file.write(f"File analysed: {filename}\n")
        file.write(f"Analysis date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n")
        #Delar upp mina sections och data sp jag kan skriva ut all min data
        for section, data in sections.items():
            file.write(section.upper() + "\n")
            file.write("-" * 30 + "\n")
            #Delar upp min data så jag får mitt keyValue och mitt själva värde
            for key, value in data.items():
                file.write(f"{key}: {value}\n")
            file.write("\n")

    file.write("=" * 60 + "\n")
    file.write("End of Analysis Report\n")
    file.write("=" * 60 + "\n")
    file.close()

    print(f"Results exported to {path}")

def amount_letters(line,letter_counter):
    line = line.split()
    for word in line:
<<<<<<< Updated upstream
        if word.isalpha():
            for ch in word:
                if ch in letter_counter:
                    letter_counter[ch] += 1
                else:
                    letter_counter[ch] = 1
=======
        for ch in word:
            if ch in letter_counter:
                letter_counter[ch] += 1
            else:
                letter_counter[ch] = 1

def digits(line):
    count = 0
    line.split()
    for dig in line:
        if dig.isdigit():
            count += 1

    return count
>>>>>>> Stashed changes
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
    appear_once = 0
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
            #Kollar ifall det finns en fil, om inte så går det inte köra koden
            case 2 | 3 | 4 | 5 | 6 if filename is None:
                print("No file is loaded. Pick 1 to load a file")
            case 2:
                #Printar alla värden jag vill visa i basic stats
                print("Total number of lines: ",stats["lines"])
                print("Total number of words: ",stats["words"])
                print("Total number of characters without spaces",stats["chars"])
                print("Total number of characters with spaces", stats["chars_with_spaces"])
                print("Average words per line:", round(stats["avg_wpl"]))
                print("Average characters per word: ",round(stats["avg_cpw"]))
                #skickar all data om "basic stats"
                results = save_section(results, filename, "Basic statistics", {
                "Lines": stats["lines"],
                "Words": stats["words"],
                "Characters": stats["chars"],
                "Characters with spaces": stats["chars_with_spaces"],
                "Average words per line": round(stats["avg_wpl"], 1),
                "Average characters per word": round(stats["avg_cpw"], 1)
            })
                input("Press Enter to open graph...")
                #skapar en graf
                vis_graph(filename, stats["lines"],stats["words"],stats["chars"],stats["chars_with_spaces"],stats["avg_wpl"],stats["avg_cpw"])

                input("Press Enter to continue...")
            case 3:
                #delar upp de olika delarna i mitt set så jag kan lätt skriva ut dem
                items = [(count, word) for word, count in stats["word_counts"].items()]
                #Sorterar så störst är först i nummering
                items.sort(reverse=True)
                total = stats["words"]
                #kollar ifall ordet är en bokstav
                letter_words = [word for word in stats["word_counts"] if word.isalpha()]
                #Hämtar största och minsta ordet
                longest = max(letter_words, key=len)
                shortest = min(letter_words, key=len)
                #sparar lite utan datan som vi ska skriva ut
                word_data = {
                    "Unique words": len(stats["word_counts"]),
                    "Words appearing only once": appear_once,
                    "Longset word": longest,
                    "Shortest word": shortest
                }
                print(f"Longest word: {longest} ({len(longest)} characters)")
                print(f"Shortest word: {shortest} ({len(shortest)} characters)")
                print("Top 10 most common words:")
                #Delar upp min "items" i två delar men jag numrerar den också så jag kan skriva ut vilken plats den är på.
                for place, (count, word) in enumerate(items[:10], start=1):
                    #räknar ut % hur vanlig varje TOP 10 ord är.
                    percent = count / total * 100
                    print(f"{place:>2}. {word:<12} {count:>7,} times ({percent:>4.1f}%)")
                    #lägger in min tabel om vanligaste orden i min data som skickas till resultat.
                    word_data[f"{place:>2}. {word:<12}"] = f"{count:>7,} times ({percent:>4.1f}%)"
                print(len(stats["word_counts"]))
                #kollar vilka ord som endast kommer fram en gång.
                for count, word in items:
                    if count == 1:
                        appear_once += 1
                print(appear_once)

                #sparar all data från case 3
                results = save_section(results, filename, "Word analysis", word_data)
                
                input("Press Enter to continue...")
            case 4:
                print("4")
                input("Press Enter to continue...")
            case 5:
<<<<<<< Updated upstream
                letters = [(letter_count, letter) for letter , letter_count in stats["letter_counter"].items()]
                letters.sort(reverse=True)
                for place, (letter_count, letter) in enumerate(letters[:10], start=1):
                    percent_letters = letter_count / stats["chars"] * 100
                    print(f"{place:>2}. {letter:<12} {letter_count:>7,} times ({percent_letters:>4.1f}%)")
=======
                print("5")
                letters = [(count, letters) for letters , count in stats["letter_counter"].items()]
                #alla spaces
                print(stats["chars"])
                print(stats["chars_with_spaces"])
                total_letters = stats["chars"]
                letters.sort(reverse=True)
                #Top 10 vanligaste bokstäverna i texten.
                for place, (count, letters) in enumerate(letters[:10], start=1):
                    percent_letters = count / total_letters * 100
                    print(f"{place:>2}. {letters:<12} {count:>7,} times ({percent_letters:>4.1f}%)")
>>>>>>> Stashed changes
                input("Press Enter to continue...")
            case 6:
                #Skapar en txt fil med all data som man gått igenom.
                export_txt(results,filename)
            case 7:
                #Avslutar programmet genom att sätta min "running" som false
                print("Thank you for using Text Analyser!")
                running = False
            #Gör så jag endast kan skriva mellan 1-7
            case _:
                print("invalid choice: pick between 1-7")



main()