import os
from datetime import datetime

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

# Call Django's setup to configure the settings
import django
django.setup()


from research.models import Project, History, BaseProject

data = {
	"table": "research_history",
	"rows":
	[
		{
			"name": "STAR2014 program",
			"subject": "&#34;Real-Time Damage Monitoring Based Wireless Nano-Sensor Networks for Industrial and Military Applications&#34;, STAR2014 Program",
			"content": "Science and Technology Amicable Research (STAR) 2014\r\n\r\nTitle of Project: &#34;Real-Time Damage Monitoring Based Wireless Nano-Sensor Networks for Industrial and Military Applications&#34;\r\n\r\nCollaborating Organization: Research Center of Automatic of Nancy (CRAN)-CNRS, University of Lorraine, BP 239, 54500 Vandoeuvre, France",
			"tcp_ip": "202.31.137.197",
			"write_date": "2014-01-22 11:08:57",
			"update_date": "2014-01-22 11:08:57",
			"visit": 1631,
			"file1": "STAR2014_Project Submission-ver.2.docx",
			"file2": ""
		},
		{
			"name": "OceanIT",
			"subject": "Ocean science research is key for a sustainable future",
			"content": "over 70% earth is covered with water. diverse organisms and minerals are available in them. the article with the link below expresses the to pay attention to the ocean for a sustainable future.\r\n\r\n\r\n\r\nhttps://www.nature.com/articles/s41467-018-03158-3",
			"tcp_ip": "202.31.137.130",
			"write_date": "2018-05-14 12:55:53",
			"update_date": "2014-01-22 11:08:57",
			"visit": 938,
			"file1": "",
			"file2": ""
		},
		{
			
			"subject": "the reality of 5G for the Marine Industry",
			"content": "The coming of 5G has been anticipated by many including the military, commerce, Transport, entertainment etc. but not much has been talked about how 5G is going to affect the marine industry. the link below is to examing the reality of 5G for the Marine Industry.\r\n\r\n\r\nhttps://superyachttechnology.com/2018/03/12/what-is-the-reality-of-5g-for-the-marine-industry/",
			"tcp_ip": "202.31.137.130",
			"write_date": "2018-05-21 15:10:59",
			"update_date": "2014-01-22 11:08:57",
			"visit": 1094,
			"file1": "",
			"file2": ""
		},
		{
			
			"subject": "WIOTC-2018 World Internet Of Things Convention (2018 WIOTC)",
			"content": "The World Internet of Convention (WIOTC) is the world&#39;s only international organization of IOT&#39;s new economy. China, France, Singapore, Germany, Hong Kong, and other continents. LOGO, Chinese name, English name are all USA, China and Hong Kong.\r\n\r\nThe World Internet of Convention (WIOTC) is the annual international summit held in various countries and regions and hosted by IOT Century Convention and Exhibition Co., Ltd. More than 40 international conventions were held in succession.\r\n\r\nInitially, the concept of the world IOT and the IOT represented the &#34;wisdom revolution&#34;, invented the world&#39;s IOT&#39;s architecture and models, and proposed ideas that revolutionized IOT definitions and attributes for sustainable development.\r\n\r\n\r\n\r\nhttp://en.wiotc.org/about/?3.html",
			"tcp_ip": "202.31.137.39",
			"write_date": "2018-07-12 14:59:38",
			"update_date": "2014-01-22 11:08:57",
			"visit": 919,
			"file1": "",
			"file2": ""
		},
		{
			
			"subject": "IncoNet CA: International Cooperation Network for Central Asian Countries",
			"content": "EXPECTED START DATE: 2013&#8226;10&#8226;01\r\nEXPECTED END DATE: 2016&#8226;11&#8226;30\r\nINSTITUTE: UNU-ViE\r\nPROJECT STATUS: Closed\r\nPROJECT TYPE: Research\r\nPROJECT MANAGER : Randa Ahmed\r\n\r\nIncoNet CA is an EU funded project which aim is to strengthen the cooperation between European and Central Asia Countries on the fields of Science, Technology and Innovation (STI) while addressing some global societal challenges, namely Climate Change, Energy and Health. The project comes within the scope of the Europe’s 2020 strategy and its flagship initiative, the European Innovation Union, which is to ensure “smart, sustainable and inclusive growth”.\r\n\r\nThe Central Asia target countries of the project, Kazakhstan, Kyrgyzstan, Tajikistan, Turkmenistan and Uzbekistan, have acknowledged tremendous changes of their political and economic systems following their independence currently depicting a respectable economic development. Despite their scientific potentials on the field of STI and the existing collaboration with the EU, both parties have expressed their will to strengthen this cooperation. This mutual interest will be the driver to make optimum use of each others academic strengths, to share respective resources and to prepare the ground for a joint effort to transfer academic results to national, regional and worldwide markets, as well as to respond to major societal challenges both regions are facing.\r\n\r\nThe UNU-ViE mainly contributes to the project by supporting the mapping process of existing projects and the stakeholder landscape in the region (WP1) which will ultimately lead to a deeper analysis once potential twin partners have been identified. Furthermore, UNU-VIE supports the coordination of the different stakeholders and serves, based on its strong international experience and network, as a platform for spreading the results and the benefits of the project on a global level.\r\n\r\nThe project is a three years interdisciplinary research conducted in cooperation with 16 partners from 14 countries.\r\n\r\nhttps://unu.edu/projects/inconet-ca-international-cooperation-network-for-central-asian-countries.html#outline",
			"tcp_ip": "",
			"write_date": "2018-07-25 13:39:09",
			"update_date": "2018-07-25 13:39:22",
			"visit": 2764,
			"file1": "",
			"file2": ""
		},
		{
			
			"subject": "International Cooperation on 5G",
			"content": "The fifth generation of communications infrastructures, or 5G, is the future network infrastructure supporting the digitisation of the economic and societal activities worldwide. The European Commission strongly supports a cooperation and seeks for a global consensus and cooperation on 5G.\r\n\r\nThe future of telecommunications and computing will see a world of fully interconnected users and devices, requiring more efficient technology to be able to overcome booming traffic and security issues. The key ICT drivers need to rely on common global definition of 5G, its service characteristics and standards. Only then can we ensure (optical and wireless) seamless communications, common ways to store and access information and computing power (cloud computing), sensing the world at large (Internet of Things) and ensuring the highest security and energy efficiency standards.\r\n\r\nA global vision, standards and identification of spectrum for 5G are currently being discussed with international industrial partners under the leadership of international bodies like the 3GPP, the ITU and the Open Networking Foundation. The 5G Infrastructure Public Private Partnership (5G PPP) also plays an essential role in federating the European input into this process.\r\n\r\nThis process is also subject to international cooperation with a goal to facilitate a global consensus on future 5G standards and spectrum requirements. To that end the European Commission has established Joint Declarations on 5G with Brazil, China, Japan and South Korea so far. Cooperation agreements are also being discussed with India and the United States.\r\n\r\n\r\n\r\nEuropean Union - South Korea\r\nA Joint Declaration on Strategic Cooperation in Information Communications Technology (ICT) and 5G, agreeing to deepen exchanges in the area of Net Futures (network and communications, 5G, cloud computing) was signed by the European Commission and the Ministry of Science, ICT and future Planning (MSIP) of the Republic of Korea in June 2014.Watch video of the spokesperson&#39;s statement on the 5G agreement with Korea.\r\n\r\nThe signing of this joint declaration reaffirmed the strengthening of the agreement of the November 2013 summit meeting, where both sides agreed on promoting R&D collaboration in the area of ICT.\r\n\r\nThis Declaration was instrumental to develop joint R&I cooperation actions in the areas of 5G, Cloud and Internet of Things (IoT), which will be implemented through jointly funded R&D programs (&#39;coordinated call&#39;) in 2016. The joint Declaration also paves the way towards structured exchanges on 5G policy matters, concerning the 5G Vision, global standards and required 5G spectrum, with the objective of supporting global agreements on these issues. Also, an industry Memorandum of Understanding was signed in June 2014 between the 5G Infrastructure Public Private Partnership (5G PPP) and the 5G Forum of the South Korea, providing the necessary industrial support to these policy commitments.\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\nhttps://ec.europa.eu/digital-single-market/en/5G-international-cooperation",
			"tcp_ip": "",
			"write_date": "2018-07-30 13:57:13",
			"update_date": "2018-07-30 13:58:16",
			"visit": 1291,
			"file1": "",
			"file2": ""
		}
	]
}


base_project = BaseProject.objects.create(
    name = 'International Cooperation',
    description = 'List of our International Cooperation projects',
)

# project = Project.objects.create(
#     base_project = base_project,
#     description = 'Description'
# )


def populate():
    for row in data['rows']:
        try:
            # Assuming 'name' in the JSON corresponds to the project name
            project_name = row['name']

            # Check if the project already exists, create if not
            project, created = Project.objects.get_or_create(name=project_name, base_project=base_project, description='Project description')


            # Convert date strings to datetime objects
            write_date = datetime.strptime(row['write_date'], "%Y-%m-%d %H:%M:%S")
            update_date = datetime.strptime(row['update_date'], "%Y-%m-%d %H:%M:%S")
            

            # Create History object
            history = History.objects.create(
                project=project,
                subject=row['subject'],
                content=row['content'],
                tcp_ip=row['tcp_ip'],
                write_date=write_date,
                update_date=update_date,
                visit=row['visit'],
                file1=row['file1'],
                file2=row['file2'],
            )
        except Exception as e:
            print(f"Error creating history for row: {row}. Error: {e}")

if __name__ == '__main__':
    populate()
    print("working again")
