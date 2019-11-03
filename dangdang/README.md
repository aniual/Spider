测试爬取当当的python数据爬取

#### 使用说明

1.进行url域名分析，关键发送请求
    http://search.dangdang.com/?key=python&act=input

2.  分析网页源码信息
    ![输入图片说明](https://images.gitee.com/uploads/images/2019/1103/092843_32a45667_5215287.png "WX20191103-091735.png")

3.  每个li进行分析
    ![输入图片说明](https://images.gitee.com/uploads/images/2019/1103/092328_96b5709d_5215287.png "WX20191103-092304.png")

4.  然后可以通过xpath进行提取
    
```
title = li.xpath("./a[position()=1]/@title").extract_first()
price = li.xpath("./p[@class='price']/span[@class='search_now_price']/text()").extract_first()
author = li.xpath("./p[@class='search_book_author']/span[position()=1]/a/@title").extract_first()
date = li.xpath("./p[@class='search_book_author']/span[position()=last()-1]/text()").extract_first()
publisher = li.xpath("./p[@class='search_book_author']/span[position()=last()]/a/@title").extract_first()
detail = li.xpath("./p[@class='detail']/text()").extract_first()
```

5. 进行自动翻页，网页分析

![输入图片说明](https://images.gitee.com/uploads/images/2019/1103/092923_770ea9af_5215287.png "WX20191103-092741.png")

6.根目录中run.py中的为启动文件，不需要再终端命令中输入，并且忽略其他的日志输出

```
from scrapy import cmdline
cmdline.execute('scrapy crawl dangSpider -s LOG_ENABLED=False'.split())
```
