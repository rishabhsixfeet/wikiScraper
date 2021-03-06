from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import urllib2
soup=''
def getPremLeague(wiki):
    """
    input takes the wiki url of football club season list url is
    in form <"http://en.wikipedia.org/wiki/List_of_"+" FOotball team name_F.C."+"_seasons">
    returns a dictionary containing
    {
        'Years': a numpy array of the year of prem league match starting from 1992 to 2103
        'Wins':  a numpy array of year wise no of matches won
        'Draw':  a numpy array of year wise no of matches draw
        'Lose':  a numpy array of year wise no of matches lost
        'Position': a list containg the rank of the team in  year
        'Topscorer': a list containing the Top Goal Scorer
        'Topgoals':  a list containing the Top Goal scored by the top scorer
    }

    """
    header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
    req = urllib2.Request(wiki,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
    tabletype=""
    #print soup
    table = soup.find_all("table", { "class" : "wikitable sortable" })
    if (len(table)==0):
        table = soup.find_all("table", { "class" : "wikitable plainrowheaders" })

    if(len(table) ==0):
        table=soup.find_all("table", { "class" : "wikitable plainrowheaders sortable" })

    if(len(table)==0):
        table=soup.find_all("table", { "class" : "wikitable" })
        tabletype="wikitable"



    #print table
    print len(table)


    won=[]
    draw=[]
    lose=[]
    years=[]
    position=[]
    TopScorer=[]
    Topgoal=[]
    #print table
    for tables in table:

        for row in tables.findAll("tr"):

            cells = row.findAll("td")
            #print cells

            if len(cells) > 4:
                if(len(cells[2].text)<=2 and len(cells[0].text.encode('ascii','ignore'))>1 ):
                    print type(cells[0].text),"#",cells[0].text.encode('ascii','ignore')
                    leag=cells[0].text.encode('ascii','xmlcharrefreplace')
                    print leag
                    if("Prem" in leag or ("PL"in leag)):
                        #print type(cells[0].text),"#",cells[0].text
                        yrs=BeautifulSoup(str(row.findAll("th")))
                        if (yrs.text[1:5]!='2014'):

                            years.append(int(yrs.text[1:5]))
                            #print "++++++++++++++++++++"
                            won.append(int((cells[2].text[:2])))
                            draw.append(int(cells[3].text[:2]))
                            lose.append(int(cells[3].text[:2]))
                            position.append(str(cells[8].text[-3:]))
                                                                    # getting the lis of top scorers in  that year
                            top=cells[len(cells)-2].findAll("span")
                            topscorer=""
                            if(len(top)>=1):
                                scorer=top[0].text.split(",")
                                topscorer=scorer[1]+' '+scorer[0]        #splitting and joinning
                            else:
                               topscorer= cells[len(cells)-2].text

                            TopScorer.append(topscorer.strip())     #removed space
                            Topgoal.append(int(cells[len(cells)-1].text[:2]))
                    elif ("Premier" in  cells[1].text.encode('ascii','xmlcharrefreplace')and tabletype=="wikitable"):     #for some teams in wikipedia  the premier name is on
                                                                                                #cells[1].text.encode('ascii','xmlcharrefreplace')


                        yrs=cells[0].text.encode('ascii','xmlcharrefreplace')
                        #print  cells[0].text.encode('ascii','ignore'),yrs.text[1:5],cells[2].text[:2],cells[8].text,cells[len(cells)-2].text,cells[len(cells)-1].text

                        if (yrs[1:5]!='2014'):

                            years.append(int(yrs[:4]))
                            #print "++++++++++++++++++++"
                            won.append(int((cells[4].text[:2])))
                            draw.append(int(cells[5].text[:2]))
                            lose.append(int(cells[6].text[:2]))
                            position.append(str(cells[9].text[-3:]))
                            topscorer=cells[len(cells)-2].text
                            TopScorer.append(topscorer.strip())     #removed space

                            Topgoal.append(int(cells[len(cells)-1].text[:2]))





    Team={'Years':np.array(years),
               'Wins':np.array(won),
               'Draws':np.array(draw),
               'Lose' :np.array(lose),
               'Position':position,
               'Topscorer':TopScorer,
               'Topgoal':np.array(Topgoal),
        }
    return Team

