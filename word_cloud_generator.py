import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Read the CSV file
# csv file should have a "word" and "frequency" column
file_path = 'file.csv'

df = pd.read_csv(file_path)

# Convert the dataframe to a dictionary
word_freq = dict(zip(df['word'], df[' frequency']))

# Create the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
