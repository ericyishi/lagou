# lagou
* 使用selenium 获取职位基本信息，方便自己筛选
* 只是爬取了职位基本信息：职位、公司、行业、发布时间、基本信息、薪酬、网址
* 使用是selenium3模拟用户界面方式来获取数据
### 注意事项
* selenium3的webdriver需要自己指明其驱动路径，这里使用的chrome的
* 另外配置了无头浏览器,可以运行时候不显示浏览器
  ```
    self.chrome_options = Options()
    self.chrome_options.add_argument('--headless')
	self.driver = webdriver.Chrome(executable_path=self.chromepath,chrome_options=self.chrome_options)

  ```
* 在使用selenuim的xpath获取属性值时，需要使用方法get_attribute()
  ```
    a=li.find_element_by_xpath(".//div[@class='list_item_top']//div[@class='p_top']//a")
    item_list.append(a.get_attribute('href'))
  ```  
* CSV中文写入乱码，open文件时候指定编码为：encoding='utf-8-sig'
  ```
     with open(self.search_name + "_data.csv", "a", encoding='utf-8-sig') as f:
  ```  
### 待优化点 
  1. 运行时间
  2. 生成csv增加当前时间【已增加】
  3. 选择城市的时候，为了图省事，目前只能传入热门城市（//a[@class="hot-city-name"），没有从全国区域入口进入。
  