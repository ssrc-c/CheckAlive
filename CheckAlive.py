import asyncio, aiohttp, time, threading, argparse
from colorama import init,Fore
init(autoreset=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36'
}

version = "1.1"

def logo():
    logo0 = r'''
    
                               
  ______ _____________   ____  
 /  ___//  ___/\_  __ \_/ ___\ 
 \___ \ \___ \  |  | \/\  \___ 
/____  >____  > |__|    \___  >
     \/     \/              \/ 
                                    Version {}
                                                By  山山而川'
                                                
                                                            
'''
    colored_logo = logo0.format(version)
    colored_logo = colored_logo.replace("____", Fore.YELLOW + "____" + Fore.RESET)

    print(colored_logo)

def usage():
    print('''
        用法:
            web批量存活检测：    python CheckAlive.py -f url.txt
        参数：
            -f   --file     url文件
            -x   --xcode    要排除的响应状态码，默认状态码为200, 301, 302, 403, 404
            -a   --addcode  要添加的状态码
            -p   -proxy     127.0.0.1:7890  使用代理                           ''')


def get_parser():
    parser = argparse.ArgumentParser(usage='python CheckAlive.py -f url.txt',
                                     description='基于python3的web存活检测脚本'
                                     )
    p = parser.add_argument_group('参数')
    p.add_argument("-f", "--file", type=str, help="urls所在txt")
    p.add_argument("-x", "--xcode", type=str, help="要排除的响应码，如-x 404，即状态码为404也判定为不存活，多个参数用逗号分隔")
    p.add_argument("-a", "--addcode", type=str, help="要增加的响应码，如-a 500，即状态码为500的也判定为存活，多个参数用逗号分隔")
    p.add_argument("-p", "--proxy", type=str, help="代理，如-p 127.0.0.1:7890")
    args = parser.parse_args()
    if args.xcode:
        args.xcode = args.xcode.split(',')
    if args.addcode:
        args.addcode = args.addcode.split(',')
    return args

def check_urls(file, proxy, xcode, addcode):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36'
    }
    codeList = [200, 301, 302, 403, 404]
    if xcode:                               #删除状态码
        for c in xcode:
            if int(c) in codeList:
                codeList.remove(int(c))
    if addcode:
        for d in addcode:
            codeList.append(int(d))
 
    if proxy:
        proxy = "http://" + proxy
    else:
        proxy = None
    try:
        urls = [url.strip() if url.startswith("http://") or url.startswith("https://") else "http://" + url.strip() for url in open(file, "r", encoding="utf-8")]
    except Exception as e:
        print("打开%s文件失败：%s" %(file, e))
        return
    print(Fore.YELLOW+"[INFO]共%s个网站" % len(urls))
    lock = threading.Lock()  # 创建互斥锁
    
    async def check_url(url, sem):
        async with sem:
            
            retry_count = 2  # 设置重试次数为1，包括初始请求的次数则为2
            while retry_count > 0:
                retry_count -= 1
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, headers=headers, ssl=False, timeout=18, allow_redirects=False, proxy=proxy) as response:
                            code = response.status
                            if code in codeList:
                                print(Fore.GREEN+"[+]响应码：%s %s 存活" %(code, url))
                                with lock:
                                    with open('alive.txt', 'a', encoding='utf-8') as f:
                                        f.write(url + '\n')
                            else:
                                print(Fore.RED+"[-]响应码：%s %s die" %(code, url))
                                with lock:  
                                    with open('die.txt', 'a', encoding='utf-8') as f:
                                        f.write(url + '\n')
                            return
                except (asyncio.TimeoutError, aiohttp.ClientConnectorError) as e:
                    if retry_count == 0:
                        print(Fore.RED+"[-]%s %s" %(url,repr(e)))
                        with lock:  
                            with open('die.txt', 'a', encoding='utf-8') as f:
                                f.write(url + '\n')
                    else:
                        await asyncio.sleep(0.7)  # 重试之前等待1秒
                except Exception as e:
                    print(Fore.RED+"[-]请求异常：%s %s" %(url, repr(e)))
                    with lock:  
                        with open('die.txt', 'a', encoding='utf-8') as f:
                            f.write(url + '\n')
                    return

    async def main():
        sem = asyncio.Semaphore(100)  # 设置并发请求数量为100
        tasks = []
        for url in urls:
            tasks.append(check_url(url, sem))
        await asyncio.gather(*tasks)

    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(Fore.GREEN+"检测完成，耗时：%s 秒。存活url保存在alive.txt，不存活url保存在die.txt" % elapsed_time)

def main():
    logo()
    args = get_parser()
    if args.file:
        #print(args.file)
        check_urls(args.file, args.proxy, args.xcode, args.addcode)
    else:
        usage()   #如果没有输入任何参数则调用usage()

if __name__ == '__main__':
    main()
