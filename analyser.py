import re
from datetime import datetime, time
from collections import Counter
from pprint import pprint

#change names here, to match whatsapp chat
name1 = "person1"
name2 = "person2"
chat_location = ""


kword = "kiss"
lword = "love"
lword2 = "loving"
lword3 = "🥰"
lword4 = "❤️"
lword5 = "🔥"
lword6 = "🥵"
lword7 = "adore"
sword = "sorry"
bword1 = "baby"
bword2 = "babe"
common_words = ["it\u2019s", "it's", "don\u2019t", "don't", "was", "are", "omitted", "message", "did", "were", "got", "", "is", "-",
                "okay", "you\u2019re", "you're", "the", "i\u2019m", "i'm", "we\u2019re", "we're", "i\u2019ll", "i'll",
                "my", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on",
                "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
                "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about",
                "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
                "people", "into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "then", "now",
                "look", "only", "come", "its", "over", "think", "also", "back", "after", "use", "two", "how", "our", "work",
                "first", "well", "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us", "i", "it",
                "didn\u2019t", "didn't", "don", "you", "that", "didn", "\u200eimage", "can", "edited>", "there", "too", "deleted",
                "things", "thing", "something", "more", "i've", "i\u2019ve", "that's", "that\u2019s", "there's", "there\u2019s",
                "\u200eyou", "what's", "what\u2019s", "am", "let", "\u200e<this", "i'd", "i\u2019d", "has", "can't", "can\u2019t"]


class Message:
    def __init__(self, date: datetime.date, time: datetime.time, day: str, text: str, out_of_hours: bool = False):
        self.date = date
        self.time = time
        self.day = day
        self.text = text
        self.out_of_hours = out_of_hours  # between 22:00 -> 06:00


def in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else:
        return start <= now or now < end

def lcheck(message_text) -> int:
    llist = [lword, lword2, lword3, lword4, lword5, lword6, lword7, bword1, bword2, "babes", "handsome", "gorgeous", "honey", "😘"]
    if any(word in message_text for word in llist):
        return 1
    else:
        return 0


class Person:
    def __init__(self, name: str):
        self.name = name
        self.messages: list[Message] = []
        self.words: list[str] = []
        self.kcount: int = 0
        self.lcount: int = 0
        self.scount: int = 0
        self.bcount: int = 0

    def average_words_per_message(self):
        return len(self.words)/len(self.messages)

    def most_used(self) -> dict[str, int]:
        c = Counter(self.words)
        li = c.most_common(200)
        results = []
        for l in li:
            if l[0] in common_words:
                ...
            else:
                try:
                    x = l.split("\u2019")
                    if x[0] in common_words:
                        ...
                    else:
                        results.append(l)
                except Exception:
                    results.append(l)

        return results

    def message_stats(self):

        stats = {
            "06:00 - 10:00": 0,
            "10:00 - 14:00": 0,
            "14:00 - 18:00": 0,
            "18:00 - 22:00": 0,
            "22:00 - 06:00": 0,
            "Sunday": 0,
            "Monday": 0,
            "Tuesday": 0,
            "Wednesday": 0,
            "Thursday": 0,
            "Friday": 0,
            "Saturday": 0,
            "Sunday L": 0,
            "Monday L": 0,
            "Tuesday L": 0,
            "Wednesday L": 0,
            "Thursday L": 0,
            "Friday L": 0,
            "Saturday L": 0,
            "k count": self.kcount,
            "l count": self.lcount,
            "s count": self.scount,
            "b count": self.bcount
        }

        for message in self.messages:
            if in_between(message.time, time(6), time(10)):
                stats["06:00 - 10:00"] += 1
            elif in_between(message.time, time(10), time(14)):
                stats["10:00 - 14:00"] += 1
            elif in_between(message.time, time(14), time(18)):
                stats["14:00 - 18:00"] += 1
            elif in_between(message.time, time(18), time(22)):
                stats["18:00 - 22:00"] += 1
            elif message.out_of_hours:
                stats["22:00 - 06:00"] += 1

            if message.day == "Sunday":
                stats["Sunday L"] += lcheck(message.text)
                stats["Sunday"] += 1
            elif message.day == "Monday":
                stats["Monday L"] += lcheck(message.text)
                stats["Monday"] += 1
            elif message.day == "Tuesday":
                stats["Tuesday L"] += lcheck(message.text)
                stats["Tuesday"] += 1
            elif message.day == "Wednesday":
                stats["Wednesday L"] += lcheck(message.text)
                stats["Wednesday"] += 1
            elif message.day == "Thursday":
                stats["Thursday L"] += lcheck(message.text)
                stats["Thursday"] += 1
            elif message.day == "Friday":
                stats["Friday L"] += lcheck(message.text)
                stats["Friday"] += 1
            elif message.day == "Saturday":
                stats["Saturday L"] += lcheck(message.text)
                stats["Saturday"] += 1

        return stats

    def parse_message(self, text: str, date: str):
        components = date.split(", ", 1)
        dateobj = datetime.strptime(components[0], "%d/%m/%Y").date()
        timeobj = datetime.strptime(components[1], "%H:%M:%S").time()
        day = str(dateobj.strftime('%A'))
        out_of_hours = True if in_between(timeobj, time(22), time(6)) else False
        self.messages.append(Message(dateobj, timeobj, day, text.lower(), out_of_hours))

        words = text.lower().split(" ")
        self.words.extend(words)

        for word in words:
            if kword in word:
                self.kcount += 1
            if lword in word:
                self.lcount += 1
            if sword in word:
                self.scount += 1
            if bword1 in word:
                self.bcount += 1
            elif bword2 in word:
                self.bcount += 1

p1 = Person(name1)
p2 = Person(name2)

def process_set(text: str):
    if len(text) > 0:
        first = text.split("] ", 1)
        date_comp = first[0].rstrip()[1:-1]
        second = first[1].split(": ", 1)
        name_comp = second[0].rstrip()
        text_comp = second[1].rstrip()

        if name_comp == name1:
            p1.parse_message(text_comp, date_comp)
        else:
            p2.parse_message(text_comp, date_comp)

# put location here
with open(chat_location, "r") as file:
    lines = ""
    for line in file:
        if re.match(r'^\[\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2}]', line):
            process_set(lines)
            lines = ""
        lines += line.rstrip('\n')

print(f"{name1} total words: {len(p1.words)}")
print(f"{name2} total words: {len(p2.words)}\n")
print("-----------------------------------------\n")
print(f"{name1} average words: {p1.average_words_per_message()}")
print(f"{name2} average words: {p2.average_words_per_message()}\n\n")
print("-----------------------------------------\n")
print(f"{name1} 20 most used words:")
for x in p1.most_used():
    print(f"{x[0]}, {x[1]}")
print("\n")
print(f"{name2} 20 most used words:")
for x in p2.most_used():
    print(f"{x[0]}, {x[1]}")
print("\n\n")
print("-----------------------------------------\n")
print(f"{name1} message stats: ")
pprint(p1.message_stats())
print("\n")
print(f"{name2} message stats: ")
pprint(p2.message_stats())
