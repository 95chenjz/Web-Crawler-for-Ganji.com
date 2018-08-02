# Web-Crawler-for-Ganji.com
Crawl users' data (id, tel number, etc.) to match PIN for Target Marketing from different categories.  
分类目从赶集网爬取包括手机号在内的用户信息，与站内PIN包匹配，实现精准引流。

## 模拟浏览器点击攻克动态网页
赶集网个人二手车网也是基于动态页面的，不提供API访问。换言之，想获取用户手机号，需要点击操作：
<img width="702" alt="20180802172331" src="https://user-images.githubusercontent.com/20656587/43575329-2c766ae4-9679-11e8-8c90-c563bfa88891.png">
<img width="740" alt="20180802172429" src="https://user-images.githubusercontent.com/20656587/43575386-4eb5aaac-9679-11e8-9af0-02a1722dc169.png">
基于selenium浏览器驱动技术的接口包webdriver，可实现模拟浏览器点击。

## 使用虚拟用户代理躲避网站连接对象检测
网站服务器通过查看Headers种的Usear Agent来判断访问来源。
应对策略：在创建Request对象的时候不添加headers参数，在创建完成之后，使用add_header()的方法，添加headers。

虚拟User-agent：Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36

此方法可躲避用户验证。


爬虫结果：
![alt tag](https://user-images.githubusercontent.com/20656587/43570362-b635f31a-966c-11e8-98b1-e7a5dd127929.png "爬虫结果")

