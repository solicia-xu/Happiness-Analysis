#this python file defines functions to make website and API calls so you can recreate the clean dataset by running one notebook file (merge_df.ipynb) that calls these functions.

import pandas as pd
import requests
import os
from lxml import html
from lxml import etree
from bs4 import BeautifulSoup
 
#worldbank.ipynb function

def worldbank():

    # variables
    url = "http://api.worldbank.org/v2/"
    query_url = f"{url}countries?format=json"
    get_pages = requests.get(query_url).json()[0]['pages']
    all_pages_list = []
    country_list = []
    poverty_list = []
    region = []
    capital_city = []
    lat_long = []
    iso2code = []

    for page in range(get_pages):
        all_pages_list.append(requests.get(f'{query_url}&page={page+1}').json()[1])
    # pprint(all_pages_list)
    for y in range(len(all_pages_list)):
        for x in range(len(all_pages_list[y])):
            country_list.append(all_pages_list[y][x]['name'])
            poverty_list.append(all_pages_list[y][x]['incomeLevel']['value'])
            region.append(all_pages_list[y][x]['region']['value'])
            capital_city.append(all_pages_list[y][x]['capitalCity'])
            lat_long.append(f"{all_pages_list[y][x]['latitude']} , {all_pages_list[y][x]['longitude']}")
            iso2code.append(all_pages_list[y][x]['iso2Code'])
    # country_list
    # poverty_list
    # region
    # capital_city
    # lat_long
    #create dataframe from all derived worldbank info
    worldbank_df = pd.DataFrame({"Country": country_list,"Country Code": iso2code,"Region": region, "Poverty Level":poverty_list,"Capital City":capital_city,"Lat/Long":lat_long})

    #drop rows that are not countries
    worldbank_df = worldbank_df[worldbank_df.Region != "Aggregates"]
    worldbank_df = worldbank_df.reset_index(drop=True)
    worldbank_df['Poverty Value (1-4)'] = worldbank_df['Poverty Level']
    worldbank_df['Poverty Value (1-4)'] = worldbank_df['Poverty Value (1-4)'].replace('High income', 4)
    worldbank_df['Poverty Value (1-4)'] = worldbank_df['Poverty Value (1-4)'].replace('Upper middle income', 3)
    worldbank_df['Poverty Value (1-4)'] = worldbank_df['Poverty Value (1-4)'].replace('Lower middle income', 2)
    worldbank_df['Poverty Value (1-4)'] = worldbank_df['Poverty Value (1-4)'].replace('Low income', 1)

    return worldbank_df

#Consumer_Electronics_2019_per_country.ipynb function

def consumer_electronics():
    
    thing = {"outlook":"DMO","preview":'false',"urlSchema":"\/outlook\/000\/999\/MARKET\/REGION","requestCorporate":"\/register\/corporate","corporateOverview":"\/accounts\/corporate\/","marketDirPath":"\/outlook\/digital-markets","accessText":"Show data","currency":"","isoCodes":{"ZA":{"id":112,"name":"South Africa"},"MA":{"id":159,"name":"Morocco"},"NG":{"id":160,"name":"Nigeria"},"AO":{"id":163,"name":"Angola"},"BW":{"id":175,"name":"Botswana"},"BI":{"id":183,"name":"Burundi"},"CM":{"id":186,"name":"Cameroon"},"TD":{"id":191,"name":"Chad"},"CG":{"id":199,"name":"Republic of the Congo"},"BJ":{"id":205,"name":"Benin"},"GQ":{"id":210,"name":"Equatorial Guinea"},"ET":{"id":211,"name":"Ethiopia"},"GA":{"id":222,"name":"Gabon"},"GM":{"id":224,"name":"Gambia"},"GH":{"id":226,"name":"Ghana"},"GN":{"id":234,"name":"Guinea"},"CI":{"id":243,"name":"Ivory Coast"},"KE":{"id":247,"name":"Kenya"},"LS":{"id":253,"name":"Lesotho"},"MG":{"id":259,"name":"Madagascar"},"MW":{"id":260,"name":"Malawi"},"MU":{"id":266,"name":"Mauritius"},"MZ":{"id":273,"name":"Mozambique"},"NA":{"id":275,"name":"Namibia"},"NE":{"id":286,"name":"Niger"},"RW":{"id":305,"name":"Rwanda"},"SN":{"id":315,"name":"Senegal"},"SC":{"id":316,"name":"Seychelles"},"SL":{"id":317,"name":"Sierra Leone"},"ZW":{"id":319,"name":"Zimbabwe"},"SD":{"id":322,"name":"Sudan"},"TG":{"id":328,"name":"Togo"},"TN":{"id":333,"name":"Tunisia"},"UG":{"id":337,"name":"Uganda"},"EG":{"id":340,"name":"Egypt"},"TZ":{"id":344,"name":"Tanzania"},"BF":{"id":346,"name":"Burkina Faso"},"ZM":{"id":353,"name":"Zambia"},"DZ":{"id":357,"name":"Algeria"},"CA":{"id":108,"name":"Canada"},"US":{"id":109,"name":"United States"},"AR":{"id":114,"name":"Argentina"},"BR":{"id":115,"name":"Brazil"},"MX":{"id":116,"name":"Mexico"},"CL":{"id":157,"name":"Chile"},"CO":{"id":158,"name":"Colombia"},"BO":{"id":173,"name":"Bolivia"},"BZ":{"id":177,"name":"Belize"},"CR":{"id":202,"name":"Costa Rica"},"CU":{"id":203,"name":"Cuba"},"DO":{"id":207,"name":"Dominican Republic"},"EC":{"id":208,"name":"Ecuador"},"SV":{"id":209,"name":"El Salvador"},"GT":{"id":233,"name":"Guatemala"},"GY":{"id":235,"name":"Guyana"},"HT":{"id":236,"name":"Haiti"},"HN":{"id":239,"name":"Honduras"},"JM":{"id":244,"name":"Jamaica"},"NI":{"id":285,"name":"Nicaragua"},"PA":{"id":295,"name":"Panama"},"PY":{"id":297,"name":"Paraguay"},"PE":{"id":298,"name":"Peru"},"SR":{"id":323,"name":"Suriname"},"UY":{"id":347,"name":"Uruguay"},"SA":{"id":110,"name":"Saudi Arabia"},"IL":{"id":111,"name":"Israel"},"CN":{"id":117,"name":"China"},"HK":{"id":118,"name":"Hong Kong"},"IN":{"id":119,"name":"India"},"ID":{"id":120,"name":"Indonesia"},"JP":{"id":121,"name":"Japan"},"MY":{"id":122,"name":"Malaysia"},"PH":{"id":123,"name":"Philippines"},"SG":{"id":124,"name":"Singapore"},"KR":{"id":125,"name":"South Korea"},"TH":{"id":126,"name":"Thailand"},"VN":{"id":127,"name":"Vietnam"},"BH":{"id":167,"name":"Bahrain"},"BD":{"id":168,"name":"Bangladesh"},"BT":{"id":172,"name":"Bhutan"},"BN":{"id":181,"name":"Brunei Darussalam"},"MM":{"id":182,"name":"Myanmar"},"KH":{"id":185,"name":"Cambodia"},"LK":{"id":190,"name":"Sri Lanka"},"IR":{"id":241,"name":"Iran"},"IQ":{"id":242,"name":"Iraq"},"KZ":{"id":245,"name":"Kazakhstan"},"JO":{"id":246,"name":"Jordan"},"KW":{"id":249,"name":"Kuwait"},"KG":{"id":250,"name":"Kyrgyzstan"},"LA":{"id":251,"name":"Laos"},"LB":{"id":252,"name":"Lebanon"},"MN":{"id":268,"name":"Mongolia"},"OM":{"id":274,"name":"Oman"},"NP":{"id":277,"name":"Nepal"},"PK":{"id":294,"name":"Pakistan"},"TL":{"id":301,"name":"Timor-Leste"},"QA":{"id":303,"name":"Qatar"},"TJ":{"id":327,"name":"Tajikistan"},"AE":{"id":332,"name":"United Arab Emirates"},"TM":{"id":334,"name":"Turkmenistan"},"UZ":{"id":348,"name":"Uzbekistan"},"AU":{"id":107,"name":"Australia"},"NZ":{"id":161,"name":"New Zealand"},"FJ":{"id":216,"name":"Fiji"},"PG":{"id":296,"name":"Papua New Guinea"},"TR":{"id":113,"name":"Turkey"},"AT":{"id":128,"name":"Austria"},"BE":{"id":129,"name":"Belgium"},"BG":{"id":130,"name":"Bulgaria"},"HR":{"id":131,"name":"Croatia"},"CZ":{"id":132,"name":"Czechia"},"DK":{"id":133,"name":"Denmark"},"EE":{"id":134,"name":"Estonia"},"FI":{"id":135,"name":"Finland"},"FR":{"id":136,"name":"France"},"DE":{"id":137,"name":"Germany"},"GR":{"id":138,"name":"Greece"},"HU":{"id":139,"name":"Hungary"},"IE":{"id":140,"name":"Ireland"},"IT":{"id":141,"name":"Italy"},"LV":{"id":142,"name":"Latvia"},"LT":{"id":143,"name":"Lithuania"},"NL":{"id":144,"name":"Netherlands"},"NO":{"id":145,"name":"Norway"},"PL":{"id":146,"name":"Poland"},"PT":{"id":147,"name":"Portugal"},"RO":{"id":148,"name":"Romania"},"RU":{"id":149,"name":"Russia"},"RS":{"id":150,"name":"Serbia"},"SK":{"id":151,"name":"Slovakia"},"SI":{"id":152,"name":"Slovenia"},"ES":{"id":153,"name":"Spain"},"SE":{"id":154,"name":"Sweden"},"CH":{"id":155,"name":"Switzerland"},"GB":{"id":156,"name":"United Kingdom"},"AZ":{"id":165,"name":"Azerbaijan"},"AM":{"id":169,"name":"Armenia"},"BA":{"id":174,"name":"Bosnia and Herzegovina"},"BY":{"id":184,"name":"Belarus"},"CY":{"id":204,"name":"Cyprus"},"GE":{"id":223,"name":"Georgia"},"IS":{"id":240,"name":"Iceland"},"LU":{"id":257,"name":"Luxembourg"},"MT":{"id":263,"name":"Malta"},"MD":{"id":269,"name":"Moldova"},"ME":{"id":270,"name":"Montenegro"},"UA":{"id":338,"name":"Ukraine"},"MK":{"id":339,"name":"North Macedonia"},"AL":{"id":355,"name":"Albania"}},"current":{"market":{"id":251,"name":"Consumer Electronics"},"region":{"id":100,"name":"worldwide"},"brand":{"id":"","name":""}}}
    country_names = []
    country_ids = []
    country_code = []
    for key, value in thing['isoCodes'].items():
        country_names.append(value['name'])
        country_ids.append(value['id'])
        country_code.append(key)
    CountryRevenueInfo = pd.DataFrame(country_ids, index = country_names)
    CountryRevenueInfo=CountryRevenueInfo.rename(columns={0:"Country ID"})
    CountryRevenueInfo['Country Code'] = country_code
    CountryRevenue2019 = CountryRevenueInfo.copy(deep=True)
    CountryRevenue2019['Year']="2019"
    CountryRevenue2019['Revenue ($M)']=""
    for index, row in CountryRevenueInfo.iterrows():
        #print(row['Country ID'])
        page = requests.get('https://www.statista.com/outlook/251/' + str(row['Country ID']) + '/consumer-electronics/worldwide')
        tree = html.fromstring(page.content)
        revenue = tree.xpath('//div[@class="font-size-xl text-light margin-top-5"]/text()')
        word=revenue[0].split('$')
        money = word[1].split('m')
        #print(money[0])
        CountryRevenue2019.loc[[index],['Revenue ($M)']] = money[0]
    CountryRevenue2018 = CountryRevenueInfo.copy(deep=True)
    CountryRevenue2017 = CountryRevenueInfo.copy(deep=True)
    CountryRevenue2017['Year'] = '2017'
    CountryRevenue2018['Year'] = '2018'
    CountryRevenue2017['Revenue ($M)']=""
    CountryRevenue2018['Revenue ($M)']=""
    for index, row in CountryRevenueInfo.iterrows():
        #print(row['Country ID'])
        page = requests.get('https://www.statista.com/outlook/251/' + str(row['Country ID']) + '/consumer-electronics/worldwide')
        data = page.text
        soup = BeautifulSoup(data,features="lxml")
        theclass = soup.find("div",'cChart cContainer active revenue')
        theclass['data-highcharts']
        split1 = theclass['data-highcharts'].split('\"data\":[')
        split2 = split1[1].split(']}]')
        split3 = split2[0].split(',')
        CountryRevenue2017.loc[[index],['Revenue ($M)']] = split3[0]
        CountryRevenue2018.loc[[index],['Revenue ($M)']] = split3[1]
#print (CountryRevenueInfo)
    CountryRevenueInfo = pd.concat([CountryRevenue2017,CountryRevenue2018,CountryRevenue2019], ignore_index = False, sort=True)

    CountryRevenueInfo['Revenue ($M)'] = (CountryRevenueInfo['Revenue ($M)']).str.replace(',','').astype(float)
    CountryRevenueInfo['Year'] = (CountryRevenueInfo['Year']).astype(float)

    
    return CountryRevenueInfo

#worldpop.ipynb function

def worldpop():
    url = "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&per_page=20000"
    country_list = []
    iso2code = []
    pop_list = []
    year = []

    response = requests.get(url).json()[1]

    for x in range(len(response)):
        iso2code.append(response[x]['country']['id'])
        country_list.append(response[x]['country']['value'])
        year.append(response[x]['date'])
        pop_list.append(response[x]['value'])
    worldpop_df = pd.DataFrame({"Country": country_list,"Country Code": iso2code,"Population": pop_list, "Year":year})
    worldpop_df = worldpop_df[worldpop_df.Population > 0]
    worldpop_df['Year']= worldpop_df['Year'].astype(float)
    return worldpop_df