import urllib.request
import json
import time

def getWebRequest(url):
	# 构建了两个代理Handler，一个有代理IP，一个没有代理IP urllib.request.ProxyHandler
	httpproxy_handler = urllib.request.ProxyHandler({"https": "10.23.5.105:3128"})
	nullproxy_handler = urllib.request.ProxyHandler({})
	header={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
	
	proxySwitch = True #定义一个代理开关
	if proxySwitch:
		opener = urllib.request.build_opener(httpproxy_handler)
	else:
		opener = urllib.request.build_opener(nullproxy_handler)
	urllib.request.install_opener(opener)
	return urllib.request.urlopen(url).read().decode("utf8")
	
	#request = urllib.request.Request(url,headers=header)
	#response = opener.open(request)
	#html = response.read()
	#return html.decode('utf-8')

if __name__ == '__main__':
	list1 = [
	'1002261',		#1 talkweb
	'1002415',		#2 HaiKanWeiShi
	#'0600104',		#3 ShangQi
	'1002661',		#4 KeMing
	'1002594',		#5 BYD
	'0600476',		#6 XianYou
	#'1002352',		#7 SF
	'1300433',		#8 LanShi
	'0601577'			#9 CSBank
	]
	list2 = [
	12,				#1
	35,				#2
	#-17,			#3
	-12.5,		#4
	-48,			#5
	-12.5,		#6
	#-40,			#7
	-15,			#8
	-7.5			#9
	]		#预警值超过闪烁显示
	#url = "https://api.money.126.net/data/feed/0000001,0601577,1002415,1002261,1002594,0600518,money.api?callback=data"
	url = 'https://api.money.126.net/data/feed/0000001,'+str(list1)[1:len(str(list1))-1].replace('\'','').replace(' ','')+',money.api?callback=data'
	firstRun = True
	while 1 == 1 :
		html = getWebRequest(url)
		data2 = json.loads(html[5:len(html)-2])
		count = 0
		priceStr = ''
		yesPrStr = ''
		while count < len(list1):
			color = 30			#字体颜色：30（黑色）31（红色）32（绿色）37（白色）34（蓝色）35（洋 红）
			style = '0'			#显示方式: 0（默认值）7（高亮）22（非粗体）4（下划线）5（闪烁）
			if(data2[list1[count]]['arrow'] == '\u2191'):
				color = 37
			else:
				color = 32
			if(list2[count] > 0):
				if(data2[list1[count]]['price'] >= list2[count]):
					style = '4'
				else:
					style = '0'			
			if(list2[count] < 0):
				if(data2[list1[count]]['price'] <= (0-list2[count])):
					style = '4'
				else:
					style = '0'		
				
			if((data2[list1[count]]['percent'] >= 0.065) | (data2[list1[count]]['percent'] <= -0.065)):
				style = style + ';7'
			priceStr = priceStr + '[' + str(count + 1) + ']' + '\033['+str(style)+';'+str(color)+';40m'+str(data2[list1[count]]['price'])+'\033[0m' + ' '
			yesPrStr = yesPrStr + '[' + str(count + 1) + ']' + str(data2[list1[count]]['yestclose']) + ' '
			count = count + 1	
		
		price = data2['0000001']['arrow'] + ' ' + str(data2['0000001']['percent']*100).replace('-','')[0:5]
		wait_time = 99
		coun_time = 0
		if(firstRun):
			print('\t     ' + yesPrStr)
			firstRun = False
		while(coun_time < wait_time):
			h = '' if wait_time - coun_time > 9 else '0'
			print (' %s %s  %s\t\t  \r' % (h + str(wait_time - coun_time),price,priceStr),end = "")	
			coun_time = coun_time + 1
			time.sleep( 1 )
