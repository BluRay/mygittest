import urllib.request
import json
import time

def getWebRequest(url):
	response = urllib.request.urlopen(url)
	html = response.read()
	return html.decode('utf-8')

if __name__ == '__main__':
	list1 = ['0601577','1002415','1002261','1002594','0600518']		#代码
	list2 = [9.8,31,-4.95,0,0]										#预警值超过闪烁显示
	#url = "https://api.money.126.net/data/feed/0000001,0601577,1002594,1002415,money.api?callback=data"
	url = 'https://api.money.126.net/data/feed/0000001,'+str(list1)[1:len(str(list1))-1].replace('\'','').replace(' ','')+',money.api?callback=data'
	while 1 == 1 :
		html = getWebRequest(url)
		data2 = json.loads(html[5:len(html)-2])
		count = 0
		priceStr = ''
		while count < len(list1):
			color = 30			#字体颜色：30（黑色）31（红色）32（绿色）37（白色）34（蓝色）35（洋 红）
			style = '0'			#显示方式: 0（默认值）1（高亮）22（非粗体）4（下划线）5（闪烁）
			if(data2[list1[count]]['arrow'] == '\u2191'):
				color = 37
			else:
				color = 35
			if(list2[count] > 0):
				if(data2[list1[count]]['price'] >= list2[count]):
					style = '5'
				else:
					style = '0'			
			if(list2[count] < 0):
				if(data2[list1[count]]['price'] <= (0-list2[count])):
					style = '5'
				else:
					style = '0'		
				
			if((data2[list1[count]]['percent'] >= 0.06) | (data2[list1[count]]['percent'] <= -0.06)):
				style = style + ';7'
			priceStr = priceStr + '\033['+str(style)+';'+str(color)+';40m'+str(data2[list1[count]]['price'])+'\033[0m' + ' '
			count = count + 1	
		
		price = data2['0000001']['arrow'] + ' ' + str(data2['0000001']['percent'])
		print (' %s  %s\r' % (price,priceStr),end = "")	
		time.sleep( 120 )
