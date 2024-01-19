

import os


# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

# Call Django's setup to configure the settings
import django
django.setup()

# from works.models import WeeklyReport
from publications.models import Book


data = {
	"table": "publications_book",
	"rows":
	[
		{
			"title": "Industrial Fieldbus Networks(산업용 필드버스 통신망)(공저, 2004년, 성안당)]",
			
			"write_date": "2008-03-02 14:01:19",
			"update_date": "2020-01-19 18:01:42",
			"visit": 3447,
			"ref": "200803020001"
		},
		{
			"title": "DeviceNet Programming: Systematic analysis and Design(디바이스넷 프로그래밍: 체계적 분석에서 실습까지), (김동성, 청문각, 2010)",
			
			"write_date": "2008-03-02 14:02:47",
			"update_date": "2020-01-19 18:01:08",
			"visit": 2779,
			"ref": "200803020002"
		},
		{
			"title": "Understanding and Programmimg of MMS(국제생산 메시지 규약의 이해와 응용 프로그래밍)   (권욱현, 김동성)  (저서, 2008년 7월, ohm사)",
			
			"write_date": "2008-03-02 15:22:20",
			"update_date": "2020-01-19 18:00:34",
			"visit": 3158,
			"ref": "200803020003"
		},
		{
			"title": "Essentials of Communication System Engineering(통신공학의 기초) (역서, 2007년, 인터비젼)",
			
			"write_date": "2008-03-02 15:22:32",
			"update_date": "2020-01-19 17:59:58",
			"visit": 5339,
			"ref": "200803020004"
		},
		{
			"title": "[ 월간제어계측: 전력선 통신 기반의 응용 시스템 및 개발 현황 (Trends of Power Line Communication Systems)(김동성, April, 2001) ]",
			
			"write_date": "2008-04-02 10:11:38",
			"update_date": "2012-12-25 21:19:30",
			"visit": 1356,
			"ref": "200804020001"
		},
		{
			"title": "[ KISTI : 미래선도기술 이슈분석 - 산업용무선필드버스(Wireless Fieldbus Technologies) (October, 2006) ]",
			"write_date": "2008-04-02 10:55:55",
			"update_date": None,
			"visit": 1288,
			"ref": "200804020002"
		},
		{
			"title": "[ KISTI : 무선통신의 미래(Furture of Wireless Networks) (김동성, 2005) ]",
			"write_date": "2008-04-02 10:57:03",
			"update_date": None,
			"visit": 1333,
			"ref": "200804020003"
		},
		{
			"title": "[ 월간전자부품: 산업용 통신망을 위한 무선통신 기술의 현황 및 분석(Recent Trends of Industrial Wireless Networks (April, 2006), 김동성 ] \r\n",
			"write_date": "2008-04-02 10:57:17",
			"update_date": None,
			"visit": 1315,
			"ref": "200804020004"
		},
		{
			"title": "[ 월간산업용통신망: 산업용무선필드버스 통신기술(Industrial Wireless Fieldbus Technology)(November, 2006), 김동성]",
			"write_date": "2008-04-02 10:57:30",
			"update_date": None,
			"visit": 1365,
			"ref": "200804020005"
		},
		{
			"title": "[ 월간산업용통신망(Industrial Communication Magazine) : &#34;발전용 통신망의 응용 메세지 규약 및 현황(Recent Trends of Application Message Specification of Power Plant Networks&#34; (2008년 3월)]",
			
			"write_date": "2008-04-02 10:57:45",
			"update_date": "2015-04-13 11:22:24",
			"visit": 1245,
			"ref": "200804020006"
		},
		{
			"title": "[주간기술동향 정보통신연구진흥원: &quot발전 시설용 MMS 부가 표준안: ICCP(MMS Companion Standard for Power Plants&quot , 김동성,  May, 2008 ]",
			"write_date": "2008-04-02 10:57:57",
			"update_date": None,
			"visit": 1262,
			"ref": "200804020007"
		},
		{
			"title": "제3회:수학적 해석 및 모의 실험(2008년 7/8월호), 제4회:응용 예를 통한 성능분석에 대한 이해(2008년 9월호) \r\n",
			"write_date": "2008-04-02 10:58:09",
			"update_date": None,
			"visit": 1249,
			"ref": "200804020008"
		},
		{
			"title": "[월간 CONTROL : &quotICCP와 MMS의 이해와 응용(ICCP and MMS)&#34; (김동성, August, 2008)]",
			
			"write_date": "2008-07-24 16:44:15",
			"update_date": "2012-12-25 21:19:02",
			"visit": 2616,
			"ref": "200807240001"
		},
		{
			"title": "제1회:산업용 통신망 모델링 (2008년 5월호), 제2회: 성능분석 방법(2008년 6월호) \r\n\r\n",
			"write_date": "2008-10-18 14:49:10",
			"update_date": None,
			"visit": 2145,
			"ref": "200810180001"
		},
		{
			"title": "[월간산업용통신망(Industrial Communication Magazine) : 산업용 통신망 성능분석 연재물 (2008), 김동성] (Special Issues: Performance Analysis of Industrial Networks)",
			
			"write_date": "2008-10-18 14:54:50",
			"update_date": "2015-04-13 11:20:10",
			"visit": 2236,
			"ref": "200810180002"
		},
		{
			"title": "Essentials of DeviceNet TechnologyDeviceNet(통신기술의 이해와 응용), (김동성, 조익영 공저, 2009년 10월, 청문각 )",
			
			"write_date": "2009-01-17 03:30:17",
			"update_date": "2020-01-19 17:59:19",
			"visit": 3088,
			"ref": "200901170001"
		},
		{
			"title": "Practice and Essentials of Networked Embedded Systems(네트워크 기반 임베디드 시스템의 기초 및 실습) (저서, 김동성, KSI), 2012.3",
			
			"write_date": "2009-11-06 10:14:36",
			"update_date": "2020-01-19 17:58:31",
			"visit": 2847,
			"ref": "200911060001"
		},
		{
			"title": "[월간자동화기술(Automation Technology Magazine), 무선 필드버스 기술의 설계 방법 및 현황(Design Scheme of Wireless Fieldbus), 김동성,  May, 2011",
			
			"write_date": "2011-04-18 16:34:19",
			"update_date": "2015-04-13 11:18:44",
			"visit": 3182,
			"ref": "201104180001"
		},
		{
			"title": "[월간자동화기술] 무선 기술로 유선 필드버스 한계를 넘다. 2012년 5월호",
			
			"write_date": "2012-06-13 17:09:38",
			"update_date": "2012-12-25 21:25:04",
			"visit": 5951,
			"ref": "201206130001"
		},
		{
			"title": "[월간자동화기술] 산업용 무선 제어망 기술 ISA100.11a 무선 제어망 2012년 6월호",
			
			"write_date": "2012-06-13 17:19:11",
			"update_date": "2014-02-26 11:51:22",
			"visit": 5970,
			"ref": "201206130002"
		},
		{
			"title": "[PlantTech] 무선 제어망 기술 통한 효율적인 산업공장 적용 가능성 2012년",
			
			"write_date": "2012-06-25 20:21:41",
			"update_date": "2012-12-25 21:25:39",
			"visit": 2215,
			"ref": "201206250001"
		},
		{
			"title": "[월간자동화기술] Wireless HART 무선 제어망 기술 2012년 7월호",
			
			"write_date": "2012-07-17 10:55:20",
			"update_date": "2012-12-25 21:25:52",
			"visit": 17369,
			"ref": "201207170001"
		},
		{
			"title": "[월간자동화기술] 산업용 무선랜 기술 2012년 8월호",
			
			"write_date": "2012-08-14 11:48:25",
			"update_date": "2012-12-25 21:26:02",
			"visit": 10392,
			"ref": "201208140001"
		},
		{
			"title": "[월간자동화기술] 유무선 혼합 제어 통신망 연구사례 2012년 10월호",
			
			"write_date": "2012-10-15 22:20:54",
			"update_date": "2012-12-25 21:26:14",
			"visit": 12913,
			"ref": "201210150001"
		},
		{
			"title": "Military Real-time Networks(국방 융복합 실시간 통신망 기술),  2014, 학산 미디어",
			
			"write_date": "2014-02-16 13:44:54",
			"update_date": "2020-01-19 17:57:52",
			"visit": 3173,
			"ref": "201402160001"
		},
		{
			"title": "Industrial Network System: From Firmware to IoT(산업용 통신망 시스템), 흥릉 과학 출판사, 김동성 저, 2018. 12",
			
			"write_date": "2018-09-25 21:50:17",
			"update_date": "2020-01-19 17:25:39",
			"visit": 2074,
			"ref": "201809250001"
		},
		{
			"title": "Basics and Application of Real-time Middleware DDS(실시간 미들웨어 DDS의 기초 및 응용) , D.-S. Kim , M.Y. Son, and etc. 2019 (in preparation)",
			
			"write_date": "2018-09-25 21:51:06",
			"update_date": "2020-01-19 17:24:51",
			"visit": 1382,
			"ref": "201809250002"
		},
		{
			"title": "Industrial Sensors and Controls in Communication Networks, D.-S. Kim and H. D. Tran, Springer, 2019.",
			
			"write_date": "2019-04-02 21:06:42",
			"update_date": "2020-08-03 14:19:15",
			"visit": 1292,
			"ref": "201904020001"
		},
		{
			"title": "젯슨나노 기초 및 활용(The basics and utilization of Jetson nano.) , 2021, 유페이퍼",
			"write_date": "2022-01-03 22:42:25",
			"update_date": None,
			"visit": 531,
			"ref": "202201030001"
		},
		{
			"title": "Cooperative and Distributed Intelligent Computation in Fog Computing: Concepts, Architectures, and Frameworks,   H. D. Tran and D.-S. Kim, Springer Nature, 2023",
			
			"write_date": "2023-07-02 22:21:10",
			"update_date": "2023-07-02 22:23:16",
			"visit": 61,
			"ref": "202307020001"
		}
	]
}


def populate():
    for row in data['rows']:
        Book.objects.create(**row)

if __name__ == '__main__':
    populate()
    print("working again")