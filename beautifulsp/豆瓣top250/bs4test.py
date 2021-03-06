import bs4
import requests
import re
import openpyxl

def open_url(url):

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
    res = requests.get(url, headers=headers)
    return res


def find_movies(res):
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    movies = []
    targets = soup.find_all("div", class_="hd")
    for each in targets:
        movies.append("《" + each.a.span.text + "》")

    ranks = []
    targets = soup.find_all("span", class_="rating_num")
    for each in targets:
        ranks.append(each.text)

    messages = []
    targets = soup.find_all("div", class_="bd")
    for each in targets:
        try:
            messages.append(each.p.text.split('\n')[1].strip() + each.p.text.split('\n')[2].strip())
        except:
            continue

    result = []
    length = len(movies)
    for i in range(length):
        result.append([movies[i], ranks[i], messages[i]])

    return result


# 找出一共多少个页面
# 用两次previous_sibling是因为第一次是返回换行符
def find_depth(res):
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    depth = soup.find('span', class_='next').previous_sibling.previous_sibling.text

    return int(depth)


def save_excel(result):
    wb = openpyxl.Workbook()
    wb.guess_types = True
    ws = wb.active

    ws.append(["电影名称", "评分", "资料"])

    for each in result:
        ws.append(each)

    wb.save("豆瓣top250.xlsx")


def main():
    host = "https://movie.douban.com/top250"
    res = open_url(host)
    depth = find_depth(res)

    result = []
    for i in range(depth):
        url = host + '?start=' + str(25*i)
        res = open_url(url)
        result.extend(find_movies(res))

    save_excel(result)





if __name__ == '__main__':
    main()