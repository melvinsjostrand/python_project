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
    "sentence": {"count": 0,
                 "total_words": 0,
                 "longest": "",
                 "longest_words": 0,
                 "shortest": "",
                 "shortest_words": 0,
                 "distribution":  {"1-5": 0, "6-10": 0, "11-20": 0, "21-30": 0, "31+": 0}
                 },
    "punctuation": 0,
    "digits": 0,
    "other": {},
    "long_words": 0
    }
    current = "" #buffert till sentence funktionen


    file = open(filename, "r", encoding="utf-8")
    inside_book = True
    #går igenom hela filen rad för rad
    for line in file:
        if "*** START OF" in line:
            inside_book = True
            reset_stats(stats)
            current = ""
            continue
        if "*** END OF" in line:
            break
        if not inside_book:
            continue
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
        
        amount_letters(line,stats["letter_counter"])
        stats["punctuation"] += count_punctuation(line)
        stats["digits"] += digits(line)
        other_chars(line, stats["other"])
    file.close()

    stats["long_words"] = long_words(stats["word_counts"])

    #Det som blev över när filen tog slut.
    if current.strip():
        add_sentence(current.strip(), stats["sentence"])
    
    stats["avg_wpl"] = stats["words"] / stats["lines"] if stats["lines"] > 0 else 0
    stats["avg_cpw"] = stats["chars"] / stats["words"] if stats["words"] > 0 else 0
    return stats

def reset_stats(stats):
    stats["lines"] = 0
    stats["words"] = 0
    stats["chars"] = 0
    stats["chars_with_spaces"] = 0
    stats["punctuation"] = 0
    stats["digits"] = 0
    stats["word_counts"].clear()
    stats["letter_counter"].clear()
    stats["other"].clear()
    stats["sentence"].update({
        "count": 0,
        "total_words": 0,
        "longest": "",
        "longest_words": 0,
        "shortest": "",
        "shortest_words": 0,
        "distribution": {"1-5": 0, "6-10": 0, "11-20": 0, "21-30": 0, "31+": 0}
     })
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


#Går igenom linjer och räknar hur många av varje ord som finns.
def word_count(line,word_count):
    line = line.lower().split()
    for word in line:
        word = word.strip(".,!?;:()-_'\"“”‘’")
        if word:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1


#Går igenom en "line" och kollar när det finns ett slut
def sentence(line, current, sentence_stats):
    line = line.strip()
    closing = "\"'”’)"
    i = 0
    while i < len(line):
        char = line[i]
        current += char

        if char in ".!?":
            #tar med stängande citattecken direkt efter punkten
            while i + 1 < len(line) and line[i + 1] in closing:
                i += 1
                current += line[i]
            #meningen är slut om raden tar slut eller ett mellanslag kommer
            if i + 1 == len(line) or line[i + 1] == " ":
                add_sentence(current.strip(), sentence_stats)
                current = ""
        i += 1

    current += " "
    return current

def add_sentence(text,s):
    word_amount = len(text.split())
    if word_amount == 0:
        return

    s["count"] += 1
    s["total_words"] += word_amount

    if word_amount > s["longest_words"]:
        s["longest"] = text
        s["longest_words"] = word_amount
    if s["shortest_words"] == 0 or word_amount < s["shortest_words"]:
        s["shortest"] = text
        s["shortest_words"] = word_amount

    s["distribution"][length_group(word_amount)] += 1


def length_group(n):
    if n <= 5:
        return "1-5"
    elif n <= 10:
        return "6-10"
    elif n <= 20:
        return "11-20"
    elif n <= 30:
        return "21-30"
    return "31+"

def count_sentences(s):
    return s["count"]

def avg_words_per_sentence(s):
    if s["count"] > 0:
        return s["total_words"] / s["count"]
    else:
        return None

def sentence_analysis(stats):
    s = stats["sentence"]
    if s["count"] == 0:
        return None

    return {
        "Sentences": count_sentences(s),
        "Average words per sentence": round(avg_words_per_sentence(s), 1),
        "Longest sentence": s["longest"],
        "Longest sentence (words)": s["longest_words"],
        "Shortest sentence": s["shortest"],
        "Shortest sentence (words)": s["shortest_words"],
        "Length distribution": s["distribution"]
    }
    


#kollar ifall orden är större än 6 tecken
def long_words(word_counts):
    count = 0
    for word, amount in word_counts.items():
        if len(word) > 6:
            count += amount
    return count


#kollar alla bokstäver
def amount_letters(line, letter_counter):
    for ch in line.lower():
        if ch.isalpha():
            if ch in letter_counter:
                letter_counter[ch] += 1
            else:
                letter_counter[ch] = 1


#räknar alla skiljetecken
def count_punctuation(line):
    punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    count = 0

    for ch in line:
        if ch in punctuation:
            count += 1
    return count
#räknar antal nummer


def digits(line):
    count = 0
    for dig in line:
        if dig.isdigit():
            count += 1
    return count


#räknar tecken som inte är bokstäver, siffror, mellanslag eller Skiljetecken
def other_chars(line, other_counter):
    punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

    for ch in line.rstrip("\n"):
        if not (ch.isalpha() or ch.isdigit() or ch == " " or ch in punctuation):
            if ch in other_counter:
                other_counter[ch] += 1
            else:
                other_counter[ch] = 1


#sparar all data i blocket, kollar också filnamn och ifall resultat har någon data i sig
def save_section(results, filename, section, data):
    #kollar ifall filen inte finns i resultat. om den inte finns så rensar jag mitt resultat
    if filename not in results:
        results[filename] = {}
    results[filename][section] = data
    return results


#Skapar en ny mapp(om mappen inte finns) som sen skapar en txt fil med namnet av txtfilen vi har kollat igenom, sedan skriver ut all data som vi sparat ner
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
                #skriver ut top 10 som en snygg lista
                if key in ("top_10", "Top_10"):
                    file.write("Top 10:\n")
                    for place, (count, item) in enumerate(value, start=1):
                        file.write(f"{place:>2}. {item:<12} {count:>7,} times\n")
                #skriver ut meningsfördelningen rad för rad
                elif key == "Length distribution":
                    file.write("Length distribution:\n")
                    for interval, count in value.items():
                        file.write(f"{interval:>6}: {count:>6}\n")
                else:
                    file.write(f"{key}: {value}\n")

    file.write("=" * 60 + "\n")
    file.write("End of Analysis Report\n")
    file.write("=" * 60 + "\n")
    file.close()

    print(f"Results exported to {path}")


#Case 1
def show_file(files):
    for file in range(len(files)):
        print(file + 1,files[file])


#Case 2
def basic_stats(stats):
    long_words = stats["long_words"]
    sentence_amount = count_sentences(stats["sentence"])
    lix = 0
    if sentence_amount != 0:
        lix = (stats["words"]/sentence_amount) + ((long_words / stats["words"]) * 100)
    level, description  = lix_level(round(lix))

    return {
        "Lines": stats["lines"],
        "Words": stats["words"],
        "Characters": stats["chars"],
        "Characters with spaces": stats["chars_with_spaces"],
        "Average words per line": round(stats["avg_wpl"], 1),
        "Average characters per word": round(stats["avg_cpw"], 1),
        "LIX": round(lix, 1),
        "LIX level": level,
        "LIX description": description
    }

def lix_level(lix):
    if 0 <= lix <= 24:
        return "Very easy", "Suitable for children's books or simple texts."
    elif 25 <= lix <= 34:
        return "Easy", "Suitable for a general audience with basic reading skills."
    elif 35 <= lix <= 44:
        return "Medium", "Typical readability for novels or newspapers."
    elif 45 <= lix <= 54:
        return "Difficult", "Suitable for academic texts or technical documents."
    elif lix >= 55:
        return "Very difficult", "Suitable for specialized literature or scientific papers"

def print_basic_stats(base_stats):
    print("Total number of lines: ",base_stats["Lines"])
    print("Total number of words: ",base_stats["Words"])
    print("Total number of characters without spaces",base_stats["Characters"])
    print("Total number of characters with spaces", base_stats["Characters with spaces"])
    print("Average words per line:", round(base_stats["Average words per line"]))
    print("Average characters per word: ",round(base_stats["Average characters per word"]))
    if base_stats["LIX"] > 0:
        print(f"LIX: {base_stats["LIX"]} ({base_stats["LIX level"]})")
        print("Typical texts: ", base_stats["LIX description"])


#Skapar grafen för basic stats
def base_stats_graph(filename, base_stats):
    #delar upp grafen i två delar så att man kan se de olika värdena
    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Basic statistics for: " + filename, fontweight="bold")
    #Gör min vänsta och högra graf. väljer färg.
    averages = right.barh(["Words per line", "Characters per word"],[base_stats["Average words per line"], base_stats["Average characters per word"]],color=["gold", "plum"])
    right.bar_label(averages, padding=5)
    right.set_title("Averages")
    right.set_xlabel("Average")
    right.set_xlim(0, max(base_stats["Average words per line"], base_stats["Average characters per word"]) * 1.2)
    left.bar(["Lines", "Words", "Characters", "Characters and spaces"],
    [base_stats["Lines"], base_stats["Words"], base_stats["Characters"], base_stats["Characters with spaces"]],
    color=["skyblue", "lightgreen", "lightcoral", "purple"])
    left.set_ylabel("Count")
    left.tick_params(axis="x", labelrotation=20)
    plt.tight_layout()
    plt.show()


#CASE 3
def word_analysis(stats):
    #Gör min word_counts till två variabler så jag kan använda både key och value
    items = [(count, word) for word, count in stats ["word_counts"].items()]
    items.sort(reverse=True)
    appea_once = 0

    for count, word in items:
        if count == 1:
            appea_once += 1

    #Hämtar alla ord som har bokstäver i sig så jag kan kolla vilka som är störst o minst 
    letter_words = [word for word in stats["word_counts"] if word.isalpha()]
    #sparar all data
    return {
        "Unique words": len(set(stats["word_counts"])),
        "Word appearing only once" : appea_once,
        "Longest word": max(letter_words, key=len),
        "Shortest word": min(letter_words, key=len),
        "top_10": items[:10] 
    }


def print_word_analysis(word_data,total_words):
    print("Top 10 most common words")
    #Skriver ut mina top 10, har tre values "place", "Count", "Word" sen placerar jag ut dem. "place" funkar pga enumerate som får ett värde
    for place,(count,word) in enumerate(word_data["top_10"], start=1):
        percent = count / total_words * 100
        print(f"{place:>2}. {word:<12} {count:>7,} times ({percent:>4.1f}%)")
    #Printar all data utöver top 10
    print("Unique words:", word_data["Unique words"])
    print("Words appearing only once:", word_data["Word appearing only once"])
    print("Longest word:", word_data["Longest word"])
    print("Shortest word:", word_data["Shortest word"])

def case3_charts(total_words,stats):
    labels = []
    amount = []
    percent = []
    label = []
    colors = ['limegreen','darkorange','lightcoral','peachpuff','darkseagreen','palevioletred','firebrick','dimgrey','darkblue','indigo']

    items = [(count, word) for word, count in stats["word_counts"].items()]
    items.sort(reverse=True)


    for count, word in items[:10]:
        amount.append(count)
        labels.append(word)
        percent.append(round(count / total_words * 100,2))

    for i in range(len(labels)):
        label.append(f"{labels[i]} ({percent[i]}%)")
    
    plt.figure(figsize=(12, 6))
    plt.bar(labels, amount, label=label, color=colors)
    plt.title('Top 10 words')
    plt.xlabel('The words')
    plt.ylabel('Amount of time in text')
    plt.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
    plt.subplots_adjust(right=0.75)
    plt.show()

#Case 4

def print_sentence_analysis(data):
    total = data["Sentences"]
    print("Total number of sentences:", total)
    print("Average words per sentence:", data["Average words per sentence"])
    print(f"Longest sentence ({data['Longest sentence (words)']} words):")
    print(" ", data["Longest sentence"])
    print(f"Shortest sentence ({data['Shortest sentence (words)']} words):")
    print(" ", data["Shortest sentence"])
    print("Sentence length distribution (words):")
    for interval, count in data["Length distribution"].items():
        print(f"{interval:>6}: {count:>6} ({count / total * 100:>4.1f}%)")

def case4_chart(data):
    total = data["Sentences"]
    precent = []
    senlen = []
    intervals = []
    explode = (0.2, 0, 0, 0, 0)
    colors = ['limegreen','darkorange','lightcoral','peachpuff','darkseagreen','palevioletred']

    for interval, count in data["Length distribution"].items():
            precent.append(f"{count / total * 100:>4.1f}%)")
            senlen.append(count)
            intervals.append(interval)

   


    plt.pie(senlen, labels=intervals, autopct='%.1f%%', shadow=True, explode=explode, startangle=180, colors=colors)
    plt.title("Sentence length distribution (words)")
    plt.show()

#Case 5

def Character_analysis(stats):
    letters = [(letter_count, letter) for letter , letter_count in stats["letter_counter"].items()]
    letters.sort(reverse=True)
    total_chars = stats["chars_with_spaces"]
    letter_total = sum(stats["letter_counter"].values())
    spaces = total_chars - stats["chars"]
    digit_total = stats["digits"]
    punct_total = stats["punctuation"]
    other_total = sum(stats["other"].values())

    return {
        "Total characters": total_chars,
        "Letters": letter_total,
        "Digits": digit_total,
        "Spaces": spaces,
        "Punctuation": punct_total,
        "Other": other_total,
        "top_10": letters[:10]
    }

def print_Character_analysis(char_analysis):
    print("Character type distribution:")
    print(f"Letters:     {char_analysis["Letters"]:<8} ({char_analysis["Letters"] / char_analysis["Total characters"] * 100:.1f}%)")
    print(f"Digits:      {char_analysis["Digits"]:<8} ({char_analysis["Digits"] / char_analysis["Total characters"] * 100:.1f}%)")
    print(f"Spaces:      {char_analysis["Spaces"]:<8} ({char_analysis["Spaces"] / char_analysis["Total characters"] * 100:.1f}%)")
    print(f"Punctuation: {char_analysis["Punctuation"]:<8} ({char_analysis["Punctuation"] / char_analysis["Total characters"] * 100:.1f}%)")
    print(f"Other:       {char_analysis["Other"]:<8} ({char_analysis["Other"] / char_analysis["Total characters"] * 100:.1f}%)")
    print("Other characters found:", char_analysis["Other"])    

    for place,(count,char) in enumerate(char_analysis["top_10"], start=1):
        percent = count / char_analysis["Letters"] * 100
        print(f"{place:>2}. {char:<12} {count:>7,} times ({percent:>4.1f}%)")

def case5_charts(char_analysis,filename):
    #delar upp grafen i två delar så att man kan se de olika värdena
    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Case 5 charts:" + filename, fontweight="bold")    
    

    rightlabels = ["Letters", "Digits", "Spaces", "Punctuation", "Other"]
    rightvalues = [char_analysis[i] for i in rightlabels]

    colors = ['limegreen','darkorange','lightcoral','peachpuff','darkseagreen','palevioletred','firebrick','dimgrey','darkblue','indigo']

    top10 = char_analysis["top_10"]
    leftlabels = [char for count, char in top10]
    leftvalues = [count for count, char in top10]

    #Gör min vänsta och högra graf. väljer färg.
    right.pie(rightvalues, labels=rightlabels, colors=colors[:5], autopct='%.1f%%', shadow=True)
    right.set_title("Character types")

    left.bar(leftlabels, leftvalues, color=colors)
    left.set_title("Top 10 letters")
    left.set_ylabel("Count")

    plt.tight_layout()
    plt.show()
    



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
                show_file(files)
                filename = load_file(files)
                if filename is not None:
                    stats = file_reader(filename)
                    results = {}
            #Kollar ifall det finns en fil, om inte så går det inte köra koden
            case 2 | 3 | 4 | 5 | 6 if filename is None:
                print("No file is loaded. Pick 1 to load a file")
            case 2:
                #går igenom alla basestats och sparar det som behövs
                base_stats = basic_stats(stats)
                
                #Printar alla värden jag vill visa i basic stats
                print_basic_stats(base_stats)

                #skickar all data om "basic stats"
                results = save_section(results, filename, "Basic statistics", base_stats)

                input("Press Enter to open graph...")

                #skapar en graf
                base_stats_graph(filename, base_stats)

                input("Press Enter to continue...")

            case 3:

                word_data = word_analysis(stats)

                print_word_analysis(word_data,stats["words"])

                results = save_section(results,filename,"Word analysis",word_data)

                input("Press Enter to open graph...")

                case3_charts(stats["words"],stats)

                input("Press Enter to continue...")
            case 4:
                    sentence_data = sentence_analysis(stats)
                    print_sentence_analysis(sentence_data)
                    results = save_section(results, filename, "Sentence analysis", sentence_data)

                    input("Press Enter to open graph...")
                    case4_chart(sentence_data)

                    input("Press Enter to continue...")
            case 5:
                #Går igenom all "character analysis" som behövs för att få rätt data
                char_analysis = Character_analysis(stats)
                #Printar min data
                print_Character_analysis(char_analysis)
                #sparar ner all min data i min "results" variabel
                results = save_section(results, filename, "Character analysis", char_analysis)

                case5_charts(char_analysis,filename)

                input("Press Enter to continue...")


            case 6:
                #Skapar en txt fil med all data som man gått igenom.
                export_txt(results,filename)
                print("EXPORT DONE, FIND THE EXPORT IN THE RESULT FILE")
                input("Press Enter to continue...")
            case 7:
                #Avslutar programmet genom att sätta min "running" som false
                print("Thank you for using Text Analyser!")
                running = False
            #Gör så jag endast kan skriva mellan 1-7
            case _:
                print("invalid choice: pick between 1-7")



main()
