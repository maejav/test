from bs4 import BeautifulSoup 
import requests
import time 
from xlwt import Workbook 

class Crawler:
    def __init__(self):
       pass
    
    def get_movie_name(self):
        movie_name = self.soup.select('div.title_wrapper > h1')[0].text
        self.movie_name = movie_name.split("(")[0]
        return self.movie_name

    def get_director(self):
        director = self.soup.select('div.credit_summary_item')[0]
        soup = BeautifulSoup(str(director), 'html.parser')
        director = soup.select('a[href]')[0].text
        self.director = director
        return self.director

    def get_writers(self):
        writers = self.soup.select('div.credit_summary_item')[1]
        soup = BeautifulSoup(str(writers), 'html.parser')
        writers = soup.select('a[href]')
        writers = list(map(lambda x: x.text, writers))
        if "more" in writers[-1]:
            del writers[-1]
        self.writers = writers
        return self.writers

    def get_cast_list(self):
        cast_list = self.soup.select('table.cast_list tr td:nth-of-type(2) a[href]')
        cast_list = list(map(lambda x: x.text.replace("\n", ""), cast_list))
        self.cast_list = cast_list
        return self.cast_list

    def get_year(self):
        year = self.soup.select('span#titleYear')[0].text.replace("\n", "").replace(")", "").replace("(", "")
        self.year = year
        return self.year

    def get_foroosh(self):
        foroosh = self.soup.select('div.article#titleDetails > div.txt-block')
        soup = BeautifulSoup(str(foroosh), 'html.parser')
        foroosh = soup.findAll('div')
        foroosh = list(map(lambda x: ' '.join(x.text.replace("\n", "").split()) , foroosh))
        for item in foroosh:
            if "Country:" in item:
                self.country = item[len("Country:") : ]
            elif "Budget:" in item:
                self.budget = item[len("Budget:") :]
            
            elif "Opening Weekend USA:" in item:
                self.opening_weekend_usa = item[len("Opening Weekend USA:") + 1 : ]

            elif "Gross USA:" in item:
                self.gross_usa = item[len("Gross USA:") + 1 : ]

            elif "Cumulative Worldwide Gross:" in item:
                self.cumulative_worldwide_gross = item[len("Cumulative Worldwide Gross:") + 1 : ]

        return self.country, self.budget, self.opening_weekend_usa, self.gross_usa, self.cumulative_worldwide_gross

    def get_250_top_movies(self):
        URL = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
        content = requests.get(URL)
        self.soup = BeautifulSoup(content.text, 'html.parser')
        links = self.soup.select('tbody.lister-list > tr > td:nth-of-type(1) > a[href]')
        links = ["http://imdb.com/" + a['href'] for a in links]
        
        wb = Workbook() 
        sheet1 = wb.add_sheet('Sheet 1') 
        sheet1.write(0, 0, 'movie') 
        sheet1.write(0, 1, 'director') 
        sheet1.write(0, 2, 'writers') 
        sheet1.write(0, 3, 'year') 
        sheet1.write(0, 4, 'country')
        sheet1.write(0, 5, 'budget')
        sheet1.write(0, 6, 'opening weekend usa,') 
        sheet1.write(0, 7, 'gross usa') 
        sheet1.write(0, 8, 'cumulative world wide gross') 
        sheet1.write(0, 9, 'list of cast') 
       
        for link_index in range(len(links)):
            content = requests.get(links[link_index])
            self.soup = BeautifulSoup(content.text, 'html.parser')
            self.get_movie_name()
            self.get_director()
            self.get_writers()
            self.get_cast_list()
            self.get_year()
            self.get_foroosh()
            sheet1.write(link_index + 1, 0, self.movie_name)
            sheet1.write(link_index + 1, 1, self.director)
            sheet1.write(link_index + 1, 2, '_'.join(self.writers))
            sheet1.write(link_index + 1, 3, self.year)
            sheet1.write(link_index + 1, 4, self.country)
            sheet1.write(link_index + 1, 5, self.budget)
            sheet1.write(link_index + 1, 6, self.opening_weekend_usa)
            sheet1.write(link_index + 1, 7, self.gross_usa)
            sheet1.write(link_index + 1, 8, self.cumulative_worldwide_gross)
            sheet1.write(link_index + 1, 9, '_'.join(self.cast_list))
            wb.save("output_final.xls") 
            print("movie " + str(link_index + 1) + " crawled")

cr = Crawler()
cr.get_250_top_movies()
