"""This is a program designed to scrape the Bowdoin Orient Website
and to run a sentiment analysis of the articles.
"""
import requests #imports a library for requesting webpages
from bs4 import BeautifulSoup #imports a library for parsing html
import pickle #a library to save custom classes to a file

class Article:
    title = str("Title Not Found") #stores the title of the article as a string
    publication_date = [0] * 3 #date is stored as a list of [year, month, day]
    authors = list() #authors stored in a lkist
    text = str() #text pf the article stored as a string

    def __str__(article):
        title = article.title

        p_date = article.publication_date
        p_year = p_date[0]
        p_month = p_date[1]
        p_day = p_date[2]

        authors = article.authors

        return (title + "\n"
                + "Published: {year}-{month}-{day}".format(year = p_year,
                month = p_month, day = p_day) + '\n'
                + "By: {authors}".format(authors = str(authors))
                )

def request_year(year): #creates a list of articles from a given year
                        #returns a list of Article objects
    URL = "https://bowdoinorient.com/" + str(year) #URL of archives for a given year
    archive_request = requests.get(URL) #sends a request for the archive
    archive_html = BeautifulSoup(archive_request.content, 'html.parser') #parses the html
    search_results = archive_html.find_all('h1', class_ = 'article-title') #search for article titles
    article_links_list = list() #list for article links
    for article in search_results: #for every search result
        a_tag = article.find('a') #find the <a> tag containing the article link
        link = a_tag.get('href') #extracts the URL from the <a> tag
        article_links_list.append(link) #adds the link to the list of article links

    for link in article_links_list: #parses information for each article
                                    #creates a Article object for each article
        article_request = requests.get(link)
        article_html = BeautifulSoup(article_request.content, 'html.parser')
        article_data = Article() #creates an Article object to store information about the article




def getAuthors(article_html): #function to find the authors of a given article
    bylines = article_html.find('p', class_ = 'byline__authors')
    author_tags = bylines.find_all('a')
    authors_list = list()
    for tag in author_tags:
        author = tag.getText()
        author = author.replace("\xa0", " ")
        authors_list.append(author)

    return authors_list

def test_function(URL): #tests parsing on a single article
    test_request = requests.get(URL)
    article_html = BeautifulSoup(test_request.content, 'html.parser')
    article_data = Article() #creates an Article object to store information about the article

    article_data.authors = getAuthors(article_html)

    print(article_data)


test_function("https://bowdoinorient.com/2021/03/05/students-disappointed-confused-about-cancellation-of-off-campus-testing-program/")