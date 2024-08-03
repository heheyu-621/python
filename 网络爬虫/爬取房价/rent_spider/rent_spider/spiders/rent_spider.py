{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "c911a14c-0bdd-4ee1-86f8-012946b37bd7",
   "metadata": {},
   "outputs": [],
   "source": [
    "import scrapy\n",
    "import pandas as pd\n",
    "\n",
    "class RentSpider(scrapy.Spider):\n",
    "    name = 'rent_spider'\n",
    "    start_urls = ['https://km.58.com/chuzu/?PGTID=0d3090a7-0021-d968-f927-b8ab41a5fd6e&ClickID=4',\n",
    "                  'https://yx.58.com/chuzu/',\n",
    "                  'https://dali.58.com/chuzu/',\n",
    "                  'https://bs.58.com/chuzu/',\n",
    "                  'https://qj.58.com/chuzu/']\n",
    "\n",
    "    def parse(self, response):\n",
    "        title_tags = response.css('a.strongbox')\n",
    "        money_tags = response.css('div.money')\n",
    "        room_tags = response.css('p.room')\n",
    "\n",
    "        data = []\n",
    "        for title_tag, money_tag, room_tag in zip(title_tags, money_tags, room_tags):\n",
    "            title = title_tag.css('::text').get().strip() if title_tag else \"N/A\"\n",
    "            money = money_tag.css('::text').get().strip() if money_tag else 'N/A'\n",
    "            room = room_tag.css('::text').get().strip() if room_tag else \"N/A\"\n",
    "            data.append([money, title, room])\n",
    "\n",
    "        df = pd.DataFrame(data, columns=['价格', '租房信息', '房型'])\n",
    "        yield {'data': df}\n",
    "\n",
    "    def closed(self, reason):\n",
    "        cities = ['昆明', '玉溪', '大理', '保山', '曲靖']\n",
    "\n",
    "        for i, city in enumerate(cities):\n",
    "            file_name = f'{city}.csv'\n",
    "            data = self.crawler.stats.get_value('data', None)\n",
    "\n",
    "            if data:\n",
    "                data[i].to_csv(file_name, index=False)\n",
    "                self.logger.info(f'Saved data to {file_name}')\n",
    "            else:\n",
    "                self.logger.error('No data found to save')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
