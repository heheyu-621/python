import requests
import parsel
import csv
f = open("链家租房-义乌.csv", mode='a', encoding='utf-8', newline='')
csv_write = csv.DictWriter(f, fieldnames=["标题", "地址(小区名)", "出租类型", "房子类型", "面积", "价格", "所在区县"])
csv_write.writeheader()
# 标题、出租类型、地址、房子类型、面积、租金、地区（区县
# 画图需要：整租、合租   租金   小区名字  区县  面积
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
}
base_url = 'https://yw.lianjia.com'
start_url = 'https://yw.lianjia.com/zufang/yiwushi/pg{}'
url_list = [start_url.format(i) for i in range(1, 101)]
print(url_list)
href_lists = []
for url_s in url_list:
    response = requests.get(url=url_s, headers=headers)
    selector = parsel.Selector(response.text)
    # 获取每页房子信息的详情页链接，之后进行详情页爬取具体信息
    href_lists = href_lists + selector.xpath("//div/a[@class='content__list--item--aside']/@href").getall()
content_to_remove = 'apartment'
# # 获取的详情页链接需要加上初始的url因此使用列表推导式
# # 但因为公寓租房的详情页网页构成与一般的租房网页结构不同，会造成后续访问不便，因此将带有apartment的链接去除
href_lists = [item for item in [base_url + href for href in href_lists] if content_to_remove not in item]
# print(href_lists)
# print(len(href_lists))
visited_links=set()
# 遍历详情页列表
id = 0
for url in href_lists:
    id += 1
    response_content = requests.get(url=url, headers=headers)
    selector_c = parsel.Selector(response_content.text)
    print(url)
    # 获取标题
    title = selector_c.xpath("//div/p[@class='content__title']/text()").get().strip()
    # 获取房子地址(小区名字)
    address_name = selector_c.xpath('/html/body/div[3]/div[1]/div[10]/h1/a/text()').get()[:-2]
    # 获取出租类型
    rent_type = selector_c.xpath('//*[@id="aside"]/ul/li[1]/text()').get()
    # 获取房子类型
    home_type = selector_c.xpath('//*[@id="aside"]/ul/li[2]/text()').get()
    # 获取房子面积
    home_area = selector_c.xpath('//*[@id="info"]/ul[1]/li[2]/text()').get()
    # 获取房子租金价格
    price = selector_c.xpath('//*[@id="aside"]/div[1]/span/text()').get()
    # 获取房子所在地区县市
    county = selector_c.xpath("//p[@class='bread__nav__wrapper oneline']/a[2]/text()").get()[:-2]
    data = {
        "标题": title,
        "地址(小区名)": address_name,
        "出租类型": rent_type,
        "房子类型": home_type,
        "面积": home_area,
        "价格": price,
        "所在区县": county
    }
    csv_write.writerow(data)
    print(id, title, address_name, rent_type, home_type, home_area, price, county)
