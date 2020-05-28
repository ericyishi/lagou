from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class Lagou(object):
    def __init__(self, search_name,city):
        self.start_url = "https://www.lagou.com/jobs/list_%E6%B5%8B%E8%AF%95?labelWords=&fromSearch=true&suginput="
        self.city=city
        self.search_name = search_name
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chromepath=r'E:\installPackage\selenium_driver\chromedriver.exe'
        self.createTime=time.strftime("%Y%m%d%H%M%S", time.localtime())

        # self.driver = webdriver.Chrome(chrome_options=self.chrome_options)

        self.driver = webdriver.Chrome(executable_path=self.chromepath,chrome_options=self.chrome_options)
        self.content_header = ["positionName", "businessZones", "CreateTime", "companyShortName", "salary", "workYear"]

    def isElementExists(self, by, value):
        # 先导入异常包
        from selenium.common.exceptions import NoSuchElementException
        try:
             self.driver.find_element(by=by, value=value)
        except NoSuchElementException as e:
            print(e)
            return False
        else:
            return True

    def close_ad(self):
        time.sleep(2)
        if self.isElementExists("class name","body-btn"):
            self.driver.find_element_by_css_selector(".body-btn").click()
        # else:
        #     print("no ad")
        # .body-btn
    def choose_city(self): # 选择城市
        time.sleep(2)
        self.driver.find_element_by_xpath('//a[@class="hot-city-name" and text()="'+self.city+'"]').click()

    def get_content_list(self):  # 提取数据
        li_list = self.driver.find_elements_by_xpath('//li[contains(@class, "con_list_item")]')
        content_list = []
        for li in li_list:
            item_list = []
            # title
            item_list.append(li.find_element_by_xpath(".//div[@class='list_item_top']//a//h3").text)
            # 发布时间
            item_list.append(li.find_elements_by_xpath(".//div[@class='list_item_top']//span[@class='format-time']")[0].text)

            # 公司名
            item_list.append(li.find_elements_by_xpath(".//div[@class='list_item_top']//div[@class='company_name']/a")[0].text)
            # 行业
            industry=li.find_elements_by_xpath(".//div[@class='list_item_top']//div[@class='industry']")[0].text
            # if "," in industry:
            #     after=industry.replace(",","|")
            #     item_list.append(after)
            # else:
            #     item_list.append(industry)
            item_list.append(industry)
            # 薪酬
            item_list.append(li.find_elements_by_xpath(".//div[@class='list_item_top']//div[@class='p_bot']//span[@class='money']")[0].text)
            # 经验
            item_list.append(li.find_elements_by_xpath(".//div[@class='list_item_top']//div[@class='p_bot']//div[@class='li_b_l']")[0].text)

            # 链接
            a=li.find_element_by_xpath(".//div[@class='list_item_top']//div[@class='p_top']//a")
            item_list.append(a.get_attribute('href'))

            # print(item_list)
            content_list.append(item_list)

        # 下一页
        next_url = self.driver.find_elements_by_xpath("//span[@class='pager_next ']")
        next_url = next_url[0] if len(next_url) > 0 else None
        return content_list, next_url

    def save_content_list(self, content_list):
        with open(self.search_name + "_"+self.createTime+".csv", "a", encoding='utf-8-sig') as f:
            for content in content_list:
                print(content)
                for item in content:
                    if isinstance(item, str):
                        if  (',' in item) :
                            a=item.replace(",", "|")
                            f.write(a + ",")
                        else:
                            f.write(item+ ",")
                f.write('\n')

    def run(self):
        # 发送请求
        self.driver.get(self.start_url)
        self.close_ad()
        self.choose_city()

        #
        # # 提取数据
        content_list, next_url = self.get_content_list()
        #
        # # 保存数据
        self.save_content_list(content_list)
        #
        # # 翻页
        while next_url is not None:
        # for i in range(0,3):
            next_url.click()
            time.sleep(6)
            content_list, next_url = self.get_content_list()
            self.save_content_list(content_list)


if __name__ == '__main__':
    lagou = Lagou("测试","成都")
    lagou.run()

