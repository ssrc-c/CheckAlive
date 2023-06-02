# CheckAlive
一款小巧的web资产快速存活检测工具
# 项目背景
在平时渗透测试或者攻防演练中，通过信息收集获取到了一批域名信息，为了提高效率此时我们需要先对这批域名进行存活探测，然后再对存活的域名进行漏洞检测。此时快速、小巧的存活检测工具尤为重要。

结合自己实际的项目需求，所以就写了这个Web资产存活检测工具CheckAlive，该工具采用python3编写，通过协程实现并发请求，探测2000个url，只需40秒左右

# 工具概述
* 批量检测：只需将url写入txt中就可以
* 检测速度快：采用协程方式，速度nice。2000个url，只需40秒左右。注意：和网速有关系。网络越好，速度越快
* 误报率极低：对超时的url自动请求重试，大大降低误报
* 忽略ssl证书问题
* 自动导出：存活和不存活的url自动导出到alive.txt和die.txt中

如果帮助到了你，请赏个Stars~~嘿嘿

# 使用
## 安装依赖
> pip install -r requirements.txt

## 工具使用
将url放在txt中，带http或者不带都行
![image](https://github.com/chenchen-cpu/CheckAlive/assets/73785589/fe60b2fb-0df9-44d9-bf38-9e013e127e4b)
执行

``` python CheckAlive.py -f url.txt ```

![image](https://github.com/chenchen-cpu/CheckAlive/assets/73785589/d5675103-e6d9-48af-9d2b-d6e64954215c)
![image](https://github.com/chenchen-cpu/CheckAlive/assets/73785589/6a7c7856-69b2-4c58-b5b7-e8d9b875769d)
