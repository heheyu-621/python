import requests
import parsel
import csv

# 设置请求头信息
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
}

# 打开 CSV 文件并初始化 CSV 写入对象
with open("链家租房-义乌.csv", mode='a', encoding='utf-8', newline='') as f:
    csv_write = csv.DictWriter(f,
                               fieldnames=["标题", "地址(小区名)", "出租类型", "房子类型", "面积", "价格", "所在区县"])
    csv_write.writeheader()

    # 基础信息设置
    base_url = 'https://xm.lianjia.com/'
    start_url = 'https://xm.lianjia.com/zufang/pg{}'
    url_list = [start_url.format(i) for i in range(1, 101)]
    href_lists = []

    # 获取所有详情页链接
    for url_s in url_list:
        response = requests.get(url=url_s, headers=headers)
        selector = parsel.Selector(response.text)
        href_lists += selector.xpath("//div/a[@class='content__list--item--aside']/@href").getall()

    # 去除公寓租房链接
    content_to_remove = 'apartment'
    href_lists = [base_url + href for href in href_lists if content_to_remove not in href]

    visited_links = set()
    id = 0

    for url in href_lists:
        if url in visited_links:
            continue
        else:
            visited_links.add(url)

        id += 1
        response_content = requests.get(url=url, headers=headers)
        selector_c = parsel.Selector(response_content.text)

        # 提取信息
        title = selector_c.xpath("//div/p[@class='content__title']/text()").get().strip()
        address_name = selector_c.xpath('/html/body/div[3]/div[1]/div[10]/h1/a/text()').get()[:-2]
        rent_type = selector_c.xpath('//*[@id="aside"]/ul/li[1]/text()').get()
        home_type = selector_c.xpath('//*[@id="aside"]/ul/li[2]/text()').get()
        home_area = selector_c.xpath('//*[@id="info"]/ul[1]/li[2]/text()').get()
        price = selector_c.xpath('//*[@id="aside"]/div[1]/span/text()').get()
        county = selector_c.xpath("//p[@class='bread__nav__wrapper oneline']/a[2]/text()").get()[:-2]

        # 写入 CSV 文件
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

print("详情页信息爬取完成，已保存到链家租房-义乌.csv文件中")