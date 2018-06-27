import requests
from bs4 import BeautifulSoup
# Grabs all hero pages from main page, and scrapes each page for lvl1 & lvl40 data
# Would be simplier to grap lvl40 data from https://feheroes.gamepedia.com/Level_40_stats_table

# main hero page url
herosUrl = 'https://feheroes.gamepedia.com/Hero_list'

# grab html
herosPage = requests.get(herosUrl)
soup = BeautifulSoup(herosPage.text, 'html.parser')

# open file to write
data = open('FEHHeroData', 'w')

# found each hero url if available in game
for heroTr in soup.find_all('tr', 'hero-filter-element'):
	# check for rarity, indication of availablity
	rarity = heroTr.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling;
	if rarity.text.find('N/A') == -1:
		# grab hero page html
		heroUrl = 'https://feheroes.gamepedia.com' + heroTr.td.a.get('href')
		heroPage = requests.get(heroUrl)
		soup = BeautifulSoup(heroPage.text, 'html.parser')

		# get lvl1 table
		lvl1 = soup.find('table', 'wikitable default')
		if lvl1 != None:
			data.write(heroUrl[31:] + '\n')
			# find out how many rows there are by counting tr find_all or just ignore first row
			rows = len(lvl1.find_all('tr')) - 1
			# obtain row data
			row = lvl1.tr
			for i in range(rows):
				row = row.next_sibling
				rowTds = row.find_all('td')
				# get the stats by getting each of the td
				RARITY = rowTds[0].text
				HP = rowTds[1].string
				ATK = rowTds[2].string
				SPD = rowTds[3].string
				DEF = rowTds[4].string
				RES = rowTds[5].string
				BS = rowTds[6].string
				# write to file
				data.write('{}, {}, {}, {}, {}, {}, {}\n'.format(RARITY, HP, ATK, SPD, DEF, RES, BS))

			# get lvl40 table
			lvl40 = lvl1.next_sibling.next_sibling
			# find out how many rows there are by counting tr find_all or just ignore first row
			rows = len(lvl40.find_all('tr')) - 1
			# obtain row data
			row = lvl40.tr
			for i in range(rows):
				row = row.next_sibling
				rowTds = row.find_all('td')
				# get the stats by getting each of the td
				RARITY = rowTds[0].text
				HP = rowTds[1].string
				ATK = rowTds[2].string
				SPD = rowTds[3].string
				DEF = rowTds[4].string
				RES = rowTds[5].string
				BS = rowTds[6].string
				# write to file
				data.write('{}, {}, {}, {}, {}, {}, {}\n'.format(RARITY, HP, ATK, SPD, DEF, RES, BS))
		else:
			print('Data not yet available ', heroTr.td.a.get('href'))
	else:
		print('Not an available hero ', heroTr.td.a.get('href'))
data.close()