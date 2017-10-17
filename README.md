# 名片信息数据爬取

## 爬取信息源网站介绍

根据常识及现原购买数据类别，名片上的信息包括姓名、机构名、地址、地点、电话（手机）、邮箱、网页链接、职务名等数据。经过初步搜索，最容易获取此类信息的网站为[企业汇总大全](http://shop.99114.com/)。此网站首页`http://shop.99114.com/`为地区索引，指向全国各省市地区公司目录。在点进某一个地区后，进入某一地区全部公司目录的第一页，链接格式为`http://shop.99114.com/list/area/XXXXXX_X`。其中末尾`XXXXXX_X`是`地区代号_页码`的正则表达式。

再点进某一公司页面，则进入该公司首页，链接格式为`http://shop.99114.com/xxxxxxxx`，其中末尾`xxxxxxxx`为公司代号，8位数字。在公司首页左方可以看到所在地区：北京市 北京市 朝阳区一栏，此条目为需要爬取的第一项数据。而滑动到下方左侧边栏，可以看到“联系我们”一栏，内含姓名、手机、公司名、电话、邮箱、地址6项信息。但是因为网页中此条目经过加密，抓取到的soup对象中此6项显示为乱码，因此不能直接爬取。回到公司主页顶部，点击“联系我们”标签，进入链接`http://shop.99114.com/xxxxxxxx/ch14`，可见此页面含有姓名、手机、电话、邮箱、地址5项信息。其中邮箱一项被加密，其余四项可直接爬取。综上，可以从此网站抓取姓名、机构名、手机、电话、邮箱、地址或地点6个类别的信息。

## 数据爬取流程

由于以上6个类别的信息分布于不同位置，故不能一次同时抓取，需分次获得。根据链接格式可分以下三种途径：

- 进入地区索引页`http://shop.99114.com/list/area/XXXXXX_X`直接抓取链接字符串，获得机构名称。此过程速度较快，每次请求可抓取上百个机构名。
- 进入公司主页`http://shop.99114.com/xxxxxxxx`，抓取左侧边栏的所在地区，获得地址或地点。此过程每次请求仅能获得最多一条数据（有的公司主页没有留地址），速度较慢。
- 进入公司“联系我们”页面`http://shop.99114.com/xxxxxxxx/ch14`，抓取中间的姓名、手机、电话、地址4项信息。由于部分公司会缺省其中某几项，此过程每次请求获得0-4项信息，速度较慢。

可见上述第2、3项都需要进入公司主页进行抓取，但如果每次都以企业黄页主页作为入口`http://shop.99114.com/` → `http://shop.99114.com/xxxxxxxx` → `http://shop.99114.com/xxxxxxxx/ch14`逐个进入公司主页抓取数据，则需要发送2-3个请求，效率太低。观察链接格式，可见每个公司均有其代号且链接格式规范。因此本爬虫采用抓取信息流程如下：

1. 以首页为入口，抓取所有格式为`http://shop.99114.com/list/area/XXXXXX_X`的链接，将所有形如`XXXXXX_X`的地区页面代号保存至`all_area_pages.txt`中，确定整个企业黄页网站地区索引的总页数。
1. 读取`all_area_pages.txt`，从每个地区页面抓取机构名和该机构链接，将链接中形如`XXXXXX_X`的机构代码保存至`all_orgs_codes.txt`中。
1. 读取`codes.txt`，通过正则表达式组合得公司首页链接和“联系我们”页面链接，爬取姓名、手机、电话、邮箱、地址或地点5类信息。

## 爬虫工作原理及项目说明

爬虫实现的主文件为`Crawler.py`和`Crawler_orgs.py`，其中`Crawler.py`为抽象类，今后针对其他网站实现爬虫时可直接继承此抽象类，`Crawler_orgs.py`为针对`http://shop.99114.com/`继承实现的爬虫。项目结构如下：

```bash
crawl\  # 爬虫项目文件夹
    crawl.py            # 爬虫主函数
    Crawler.py          # 爬虫抽象类
    Crawler_orgs.py     # 爬虫实现
    all_area_pages.txt  # 存放形如http://shop.99114.com/list/area/XXXXXX_X的地区索引页
    all_orgs_codes.txt  # 存放形如xxxxxxxx的公司代号
```

### `Crawler`类方法说明

- `_get_response`传入网页链接，返回response对象，若遇到反爬虫或找不到服务器则返回None
- `_get_soup`传入网页链接，抓取其html文本，返回BeautifulSoup对象，若遇到反爬虫或找不到服务器则返回None
- `_get_links`传入网页链接，返回该网页上所有链接
- `_get_link_strings`传入网页链接，返回该网页上所有链接名称字符串
- `read_lines`传入文本文件名，读取所有行并返回至list

### Crawler_orgs类方法说明

- `_get_area_first_pages`返回每个地区索引的第一页链接，形如`http://shop.99114.com/list/area/XXXXXX_1`
- `_get_all_pages` 返回每个地区的所有页链接，形如`http://shop.99114.com/list/area/XXXXXX_X`
- `_get_org_codes` 传入地区索引页链接，返回该地区索引页上所有公司的代号
- `crawl_org_codes` 传入地区索引页链接，将该页上所有公司代号写入txt文件中保存
- `crawl_orgs_names` 传入地区索引页链接，将该页上所有公司名写入txt文件中保存
- `crawl_orgs_postals` 传入公司代号，抓取其地址并写入txt文件中保存
- `crawl_orgs_infos` 传入公司代号，抓取其姓名、手机、电话、公司名并写入txt文件中保存

各函数具体实现原理见代码注释。在爬取数据时，打开`crawl.py`消除对应行注释，并运行指令`python crawl.py`即可开始爬虫。由于逐个公司爬取效率太低，可以将`all_orgs_codes.txt`分成多份，同时开多个python终端进行爬取。

# 数据预处理及数据集构建

## 数据清洗及预处理

由上一节说明可知，分三次爬取的数据存于三个文件中：`org.txt`， `post_place.txt`， `info.txt`。其中`org.txt`为公司名，`post_place.txt`为地址或地点，消除空格及去重后即可。`info.txt`中每行数据格式为`电话 手机 姓名-公司名`。只需运行`python info.py`即可自动抽取数据，输出`name.txt`，`org.txt`，`mobile.txt`，`phone.txt`四个文件于当前路径。

### 项目结构

```bash
data\
    preprocess.py   # 预处理函数
    info.py         # 提取姓名、手机、电话、公司名
    crawled_raw\
    name.txt        # 姓名
    mobile.txt      # 手机号码
    org.txt         # 机构名
    phone.txt       # 固定电话、传真
    place.txt       # 地点
    post.txt        # 地址
seg\                # 采用THULAC或单字分割后的数据
...
seg_labeled\        # 分词且标签后数据
...
```

### `preprocess`类方法说明

- `add_label` 为数据加入制定标签
- `seg` 将所有数据加使用THUL AC分词
- `char_seg` 将所有数据单字分割
- `find_postal` 将地址和地点区分开
- `derep` 数据去重
- `clear_empty_lines` 去除空行

## 数据集构造方法

为验证数据量大小对fasttext和TextCNN模型性能的影响，需要构造不同量级的数据集，对照实验fasttext和TextCNN的效果。其中全部数据集均从爬取数据中随机不放回抽取，以保证数据不重复出现。训练、验证集比例为4:1。目前根据已有数据量确定数据集量级分别为4k:1k、25k:5k、400k:100k
