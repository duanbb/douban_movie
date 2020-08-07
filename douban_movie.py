from bs4 import BeautifulSoup
import requests
import pandas as pd

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

url_list = [
    'https://movie.douban.com/people/98909222/wish?start=0&sort=time&rating=all&filter=all&mode=list',
    'https://movie.douban.com/people/98909222/wish?start=30&sort=time&rating=all&filter=all&mode=list'
]


def get_movie_info(movie_url):
    r_movie = requests.get(movie_url, headers=HEADER)
    soup_movie = BeautifulSoup(r_movie.text, 'html.parser')

    return {
        'name': str(soup_movie.find_all('span', {'property': 'v:itemreviewed'})[0].contents[0]),
        'year': int(soup_movie.find_all('span', {'class': 'year'})[0].contents[0].replace('(', '').replace(')', '')),
        'rating': float(soup_movie.find_all('strong', {'class': 'll rating_num', 'property': 'v:average'})[0].contents[0]),
        'votes': int(soup_movie.find_all('span', {'property': 'v:votes'})[0].contents[0]),
        'url': movie_url
    }


def get_page_info(url):
    r_page = requests.get(url, headers=HEADER)
    soup_page = BeautifulSoup(r_page.text, 'html.parser')  # 'lxml'
    movies = soup_page.find_all('div', {'class': 'title'})

    for i in range(0, len(movies)):  # 3
        movies_list.append(get_movie_info(movies[i].contents[1].attrs['href']))
        print('No. ' + str(i))
    del i


if __name__ == '__main__':
    movies_list = []
    for i in range(0, len(url_list)):
        get_page_info(url_list[i])
    del i

    movies_df = pd.DataFrame(data=movies_list)

    movies_df['rating_year'] = movies_df['rating'] * movies_df['year']
    movies_df['rating_votes'] = movies_df['rating'] * movies_df['votes']
    movies_df['rating_year_votes'] = movies_df['rating'] * movies_df['year'] * movies_df['votes']

    movies_df.sort_values('rating_year_votes', ascending=False).reset_index()

    print('end')
