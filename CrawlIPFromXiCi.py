from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.keys import Keys
import random, time, pymysql
from bs4 import BeautifulSoup

# 配置信息
mysql_config = {
    'host': '你的host',
    # 需要注意的是，有些服务器不需要输入port，例如阿里云的Mysql数据库服务器
    'port': '你的port',
    'user': 'testuser',
    'password': 'aa123456',
    'db': 'test',
    'charset': 'utf8mb4'
}


# 将IP存储到MySql数据库
def save(ip):
    exist = isExist(ip)
    if exist:
        # 执行更新
        connection = pymysql.connect(**mysql_config)
        try:
            with connection.cursor() as cursor:
                sql = '''update testsimulation set
                                STATU='0'
                                 where IP='{0}' '''.format(str(ip))
                cursor.execute(sql)
                connection.commit()
        finally:
            connection.close()
    else:
        connection = pymysql.connect(**mysql_config)
        try:
            with connection.cursor() as cursor:
                sql = "insert into testsimulation(ip,statu) values('%s',0)" % (str(ip))
                cursor.execute(sql)
                connection.commit()
        finally:
            connection.close()

# 判断是否存在此IP
def isExist(ip):
    connection = pymysql.connect(**mysql_config)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM testsimulation where ip = '%s'" % (str(ip))
            cursor.execute(sql)
            results = cursor.fetchall()
            print('返回结果有[{0}]行'.format(len(results)))
            if len(results) > 0:
                return True
            else:
                return False
    finally:
        connection.close()


def test(ip):
    proxy = Proxy(
        {
            'proxyType': ProxyType.MANUAL,
            'httpProxy': ip  # 代理ip和端口
        }
    )
    # 新建一个“期望技能”，哈哈
    desired_capabilities = webdriver.DesiredCapabilities.PHANTOMJS.copy()
    # 把代理ip加入到技能中
    proxy.add_to_capabilities(desired_capabilities)
    web = webdriver.PhantomJS(
        executable_path=r'C:\Users\coolzhm\Desktop\IL Spy\phantomjs-2.1.1-windows\bin\phantomjs.exe',
        desired_capabilities=desired_capabilities
    )
    web.set_page_load_timeout(10)
    web.set_script_timeout(10)  # 这两种设置都进行才有效    # 测试一下
    try:
        web.get('http://www.dmcool.top/')
        print('用IP[{0}]测试访问，返回当前地址为[{1}]'.format(ip, web.current_url))
        if 'www.dmcool.top' in web.current_url:
            save(ip)
    except Exception as e:
        print('使用IP[{0}]测试访问出错,详细内容为：{1}'.format(ip, e))
    finally:
        web.quit()


currentUrl = 'http://www.xicidaili.com/nn/4'
driver = webdriver.PhantomJS(
    executable_path=r'C:\Users\coolzhm\Desktop\IL Spy\phantomjs-2.1.1-windows\bin\phantomjs.exe'
)
# 防止卡死，设置超时时间
driver.set_page_load_timeout(20)
driver.set_script_timeout(20)  # 这两种设置都进行才有效    # 测试一下
# 先进入第一页
driver.get(currentUrl)
while 1 == 1:
    try:
        soup = BeautifulSoup(driver.page_source, "lxml")
        trs = soup.find_all('tr')
        # 循环遍历获取IP地址
        for tr in trs:
            try:
                # 获取IP
                ip = tr.contents[3].string + ":" + tr.contents[5].string
                test(ip)
            except:
                continue
    except Exception as e:
        print('循环遍历获取IP地址出错了，详情：{0}'.format(e))
    finally:
        # 休息5秒钟
        time.sleep(5)
        # 获取下一页xpath，并点击下一页按钮
        xpath = '//*[@class="next_page"]'
        try:
            # 在ac位置单击
            ac = driver.find_element_by_xpath(xpath)
            ac.send_keys(Keys.ENTER)
            print('通过[点击方式]进入下一页[{0}]'.format(driver.current_url))
        except:
            # 如果不能使用点击进入下一页我们就通过href获取下一页地址后直接访问
            soup1 = BeautifulSoup(driver.page_source, 'lxml')
            nexts = soup1.find_all('a', class_='next_page')
            next = ''
            for a in nexts:
                next = a.get('href')
            print('通过[链接方式]进入下一页[{0}]'.format(driver.current_url))
            driver.get('http://www.xicidaili.com' + next)
