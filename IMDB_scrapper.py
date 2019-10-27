# scrap top 50 movies from IMDB (genre of your choice)
import requests
from bs4 import BeautifulSoup as soup
import csv

# insert genre
genre = input('Genre: ')

# requests IMDB web page
res = requests.get('https://www.imdb.com/search/title/?genres=' + genre)

# parse selected web page
res_soup = soup(res.text, 'html.parser')

# locate the main container
containers = res_soup.findAll('div', {'class': 'lister-item-content'})

index = 1

def filter_year(input):
    year = ''
    for char in input:
        if char.isdigit() or char == '–':
            year+= char
    return year

rows_of_data = []
# iterate through each container and append the relevant detail into a list
for container in containers:
    title = container.find('a').text
    sample_year = container.find('span',{'class','lister-item-year text-muted unbold'}).text[1:-1]
    year = filter_year(sample_year)
    try:
        length = container.find('span',{'class','runtime'}).text
    except:
        length = ''
    try:
        rating = container.find('div',{'class','inline-block ratings-imdb-rating'})['data-value']
    except:
        rating = ''
    rows = [index,title,year,length,rating]
    rows_of_data.append(rows)
    index+=1


#write data into csv
with open('Top50Movies.csv','w',newline='') as output:
    output_writer = csv.writer(output)
    output_writer.writerow(['No.','Title','Year','Length','Rating'])
    for row in rows_of_data:
        output_writer.writerow(row)
