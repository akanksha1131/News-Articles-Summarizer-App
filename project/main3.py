import os.path
import csv
from bs4 import BeautifulSoup
from newspaper import Article
from gensum import text_summarizer
from main2 import categorize_articles

# Function to download and parse articles, and save data to CSV
def download_and_save_articles(links_list, csv_file):
    article_links = []
    article_text = []
    article_summary = []
    article_titles = []
    article_img = []
    total = 0

    for link in links_list:
        try:
            article = Article(link)
            article.download()
            article.parse()
            article.nlp()
            text = article.text
            summary = text_summarizer(text)

            # Find img src
            img_src = None
            img_tags = BeautifulSoup(article.html, 'html.parser').find_all('img')
            for img_tag in img_tags:
                src = img_tag.get('src', '')
                alt = img_tag.get('alt', '')
                fetchpriority = img_tag.get('fetchpriority', '')
                if "static.toiimg." in src and alt != "TOI logo" and fetchpriority == "high":
                    img_src = src
                    break

            # Check if all fields are valid and not null
            if all(field is not None and isinstance(field, str) and field.strip() for field in [link, text, summary, img_src]):
                article_img.append(img_src)
                article_links.append(link)
                article_text.append(text)
                article_titles.append(article.title)  # Domain name as title
                article_summary.append(summary)
                total += 1
                print(total)

            if total >= 40:
                break

        except Exception as e:
            print(f"Error downloading article from {link}: {e}")
            continue  # Continue with the next iteration of the loop

    # Save data to CSV
    if article_titles:
        if os.path.exists(csv_file):
            file_size = os.path.getsize(csv_file)
            if file_size == 0:
                with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Article Title', 'Article Link', 'Article Text', 'Article Summary', 'Article Image'])
                    for i in range(len(article_titles)):
                        writer.writerow([article_titles[i], article_links[i], article_text[i], article_summary[i], article_img[i]])
                print("Data has been saved to:", csv_file)
print("All CSV files ready for display")
# Define CSV file paths
info_files = {
    0: "C:\\Users\\AKANKSHA KALE\\Desktop\\NLP_Project\\project\\india.csv",
    1: "C:\\Users\\AKANKSHA KALE\\Desktop\\NLP_Project\\project\\world.csv",
    2: "C:\\Users\\AKANKSHA KALE\\Desktop\\NLP_Project\\project\\business.csv",
    3: "C:\\Users\\AKANKSHA KALE\\Desktop\\NLP_Project\\project\\tech.csv",
    4: "C:\\Users\\AKANKSHA KALE\\Desktop\\NLP_Project\\project\\sports.csv"
}

# Example usage:
all_links = [
    "https://timesofindia.indiatimes.com/india",
    "https://timesofindia.indiatimes.com/world",
    "https://timesofindia.indiatimes.com/business",
    "https://timesofindia.indiatimes.com/technology",
    "https://timesofindia.indiatimes.com/sports"
]

domain_lists = categorize_articles(all_links)
print(domain_lists)  # Printing domain_lists for demonstration
d=['India', 'World', 'Business', 'Technology', 'Sports']

for i in range(5):
    link_list = domain_lists[d[i]]
    filepath = info_files[i]
    download_and_save_articles(link_list, filepath)
