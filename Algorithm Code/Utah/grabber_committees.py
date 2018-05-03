'''

Python script that is to grab all the articles from the source: KSL, more
specifically for the KSL politics section.

Author: Founding Fathers, Kristian Nilssen
Date: 3/15/2017

Usage:

    python grabber_ksl.py [ current_time ]

'''

import sys
import newspaper
import urllib
from article_grabbers import date_subtracter
import json
import requests
from database_interactors import mysql_committee_entry
from database_interactors import mysql_committee_person_entry
from newspaper import Article
from bs4 import BeautifulSoup
import time

def main():
    committees_info = [{"description":"Administrative Rules Review Committee","id":"SPEADM","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEADM","meetings":[],
    "members":[
    {"id":"ADAMSJS","position":"member"}
    ,{"id":"BUXTODG","position":"member"}
    ,{"id":"COLEMK","position":"member"}
    ,{"id":"DABAKJ","position":"member"}
    ,{"id":"DAVISG","position":"member"}
    ,{"id":"GREENBM","position":"chair"}
    # ,{"id":"MADSEMB","position":"member"}
    ,{"id":"MOSSCS","position":"member"}
    ,{"id":"STEPHHA","position":"chair"}
    ,{"id":"WEBBRC","position":"member"}
    ,{"id":"WHEATMA","position":"member"}]
    }
    ,{"description":"Business, Economic Development, and Labor Appropriations Subcommittee","id":"APPBEL","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=APPBEL","meetings":[
    {"mtgTime":"2017-06-22T8:00:00.000Z","mtgPlace":"25 House Building","status":"O"}],
    "members":[
    {"id":"ANDERJL","position":"member"}
    ,{"id":"BARLOSE","position":"member"}
    ,{"id":"BRAMBCS","position":"member"}
    ,{"id":"BUXTODG","position":"member"}
    ,{"id":"DAVISG","position":"member"}
    ,{"id":"GARDIA","position":"member"}
    ,{"id":"HARPEWA","position":"member"}
    ,{"id":"HENDEDM","position":"member"}
    ,{"id":"MOSSCS","position":"member"}
    ,{"id":"PETERJA","position":"member"}
    ,{"id":"PETERVL","position":"member"}
    ,{"id":"SANDASD","position":"house vice chair"}
    ,{"id":"SHIOZBE","position":"senate chair"}
    ,{"id":"WEBBRC","position":"house chair"}
    ,{"id":"WEIGHE","position":"member"}
    ,{"id":"WESTWJR","position":"member"}
    ,{"id":"WILSOBR","position":"member"}]
    }
    ,{"description":"Commission on Federalism","id":"SPECOF","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPECOF","meetings":[],
    "members":[
    {"id":"CHRISAM","position":"chair"}
    ,{"id":"CHRISKJ","position":"member"}
    ,{"id":"FILLML","position":"member"}
    ,{"id":"IVORYK","position":"chair"}
    ,{"id":"KINGBS","position":"member"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"SNOWVL","position":"member"}]
    }
    ,{"description":"Executive Appropriations Committee","id":"APPEXE","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=APPEXE","meetings":[],
    "members":[
    {"id":"ADAMSJS","position":"member"}
    ,{"id":"BRISCJK","position":"member"}
    ,{"id":"DAVISG","position":"member"}
    ,{"id":"ESCAML","position":"member"}
    ,{"id":"GIBSOFD","position":"member"}
    ,{"id":"HOLLIS","position":"member"}
    ,{"id":"HUGHEGH","position":"member"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"KINGBS","position":"member"}
    ,{"id":"KNOTWJ","position":"member"}
    ,{"id":"KNUDSPC","position":"member"}
    ,{"id":"LASTBG","position":"house vice chair"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"NIEDEWL","position":"member"}
    ,{"id":"OKERLR","position":"member"}
    ,{"id":"ROMERAY","position":"member"}
    ,{"id":"SANPED","position":"house chair"}
    ,{"id":"STEVEJW","position":"senate chair"}
    ,{"id":"VANTAKT","position":"senate vice chair"}
    ,{"id":"WILSOBR","position":"member"}]
    }
    ,{"description":"Executive Offices and Criminal Justice Appropriations Subcommittee","id":"APPEOC","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=APPEOC","meetings":[
    {"mtgTime":"2017-07-20T8:00:00.000Z","mtgPlace":"25 House Building","status":"O"}
    ,{"mtgTime":"2017-10-19T8:00:00.000Z","mtgPlace":"25 House Building","status":"O"}],
    "members":[
    {"id":"BRAMBCS","position":"member"}
    ,{"id":"CUTLEBR","position":"house vice chair"}
    ,{"id":"DAYTOM","position":"member"}
    ,{"id":"DUNNIJA","position":"member"}
    ,{"id":"FILLML","position":"member"}
    ,{"id":"HUTCHEK","position":"house chair"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"KINGBS","position":"member"}
    ,{"id":"KNUDSPC","position":"member"}
    ,{"id":"NELSOMF","position":"member"}
    ,{"id":"OKERLR","position":"member"}
    ,{"id":"QUINNT","position":"member"}
    ,{"id":"ROMERAY","position":"member"}
    ,{"id":"SNOWVL","position":"member"}
    ,{"id":"THATCDW","position":"senate chair"}
    ,{"id":"WILDEL","position":"member"}]
    }
    ,{"description":"Federal Funds Commission","id":"SPEFFC","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEFFC","meetings":[],
    "members":[
    {"id":"ANDERJL","position":"member"}
    ,{"id":"FAWSOJL","position":"member"}
    ,{"id":"FILLML","position":"vice chair"}
    ,{"id":"IVORYK","position":"chair"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"KINGBS","position":"member"}]
    }
    ,{"description":"Higher Education Appropriations Subcommittee","id":"APPHED","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=APPHED","meetings":[
    {"mtgTime":"2017-07-20T8:00:00.000Z","mtgPlace":"210 Senate Building","status":"O"}
    ,{"mtgTime":"2017-10-19T8:00:00.000Z","mtgPlace":"210 Senate Building","status":"O"}],
    "members":[
    {"id":"COLEMK","position":"member"}
    ,{"id":"DABAKJ","position":"member"}
    ,{"id":"DAWBM","position":"member"}
    ,{"id":"GROVEK","position":"house chair"}
    ,{"id":"HENDEDM","position":"member"}
    ,{"id":"IPSONDL","position":"member"}
    ,{"id":"KWANK","position":"member"}
    ,{"id":"MILESKB","position":"member"}
    ,{"id":"MILLNA","position":"member"}
    ,{"id":"OWENSD","position":"house vice chair"}
    ,{"id":"POTTEVK","position":"member"}
    ,{"id":"STANAJE","position":"member"}
    ,{"id":"STEPHHA","position":"member"}
    ,{"id":"STEVEJW","position":"member"}
    ,{"id":"VICKEEJ","position":"senate chair"}
    ,{"id":"WHEATMA","position":"member"}
    ,{"id":"WINDEM","position":"member"}]
    }
    ,{"description":"House Business and Labor Committee","id":"HSTBUS","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=HSTBUS","meetings":[],
    "members":[
    {"id":"DUCKWS","position":"member"}
    ,{"id":"DUNNIJA","position":"chair"}
    ,{"id":"FROERG","position":"member"}
    ,{"id":"GARDIA","position":"member"}
    ,{"id":"HAWKETD","position":"member"}
    ,{"id":"KNOTWJ","position":"member"}
    ,{"id":"MCKELMK","position":"member"}
    ,{"id":"PETERJA","position":"member"}
    ,{"id":"ROBERMK","position":"vice chair"}
    ,{"id":"SCHULM","position":"member"}
    ,{"id":"STANAJE","position":"member"}
    ,{"id":"WEBBRC","position":"member"}
    ,{"id":"WHEATMA","position":"member"}
    ,{"id":"WILSOBR","position":"member"}]
    }
    ,{"description":"House Economic Development and Workforce Services Committee","id":"HSTEDW","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=HSTEDW","meetings":[],
    "members":[
    {"id":"ALBRECR","position":"member"}
    ,{"id":"CHRISFL","position":"member"}
    ,{"id":"EDWARRP","position":"chair"}
    ,{"id":"MALOYC","position":"member"}
    ,{"id":"MOSSCS","position":"member"}
    ,{"id":"ROMERAY","position":"member"}
    ,{"id":"SANDASD","position":"member"}
    ,{"id":"WATKICF","position":"member"}
    ,{"id":"WESTWJR","position":"vice chair"}
    ,{"id":"WINDEM","position":"member"}]
    }
    ,{"description":"House Education Committee","id":"HSTEDU","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=HSTEDU","meetings":[],
    "members":[
    {"id":"CHRISFL","position":"member"}
    ,{"id":"COLEMK","position":"vice chair"}
    ,{"id":"CUTLEBR","position":"member"}
    ,{"id":"FAWSOJL","position":"member"}
    ,{"id":"GIBSOFD","position":"member"}
    ,{"id":"HUTCHEK","position":"member"}
    ,{"id":"LASTBG","position":"member"}
    ,{"id":"MCCAYD","position":"member"}
    ,{"id":"MOSSCS","position":"member"}
    ,{"id":"NOELME","position":"member"}
    ,{"id":"OWENSD","position":"member"}
    ,{"id":"PETERVL","position":"chair"}
    ,{"id":"POULSMH","position":"member"}
    ,{"id":"SNOWVL","position":"member"}]
    }
    ,{"description":"House Ethics Committee","id":"HSTETH","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=HSTETH","meetings":[],
    "members":[
    {"id":"ARENTPM","position":"co-chair"}
    ,{"id":"DUNNIJA","position":"member"}
    ,{"id":"GROVEK","position":"member"}
    ,{"id":"NOELME","position":"member"}
    ,{"id":"POULSMH","position":"member"}
    ,{"id":"ROMERAY","position":"member"}
    ,{"id":"SAGERD","position":"chair"}
    ,{"id":"WHEATMA","position":"member"}]
    }
    ,{"description":"House Government Operations Committee","id":"HSTGOC","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=HSTGOC","meetings":[],
    "members":[
    {"id":"ARENTPM","position":"member"}
    ,{"id":"CHAVER","position":"member"}
    ,{"id":"DAWBM","position":"member"}
    ,{"id":"MCCAYD","position":"member"}
    ,{"id":"NELSOMF","position":"member"}
    ,{"id":"PERRYLB","position":"member"}
    ,{"id":"PETERJA","position":"chair"}
    ,{"id":"PETERVL","position":"member"}
    ,{"id":"SANPED","position":"member"}
    ,{"id":"THURSNK","position":"vice chair"}]
    }
    ,{"description":"House Health and Human Services Committee","id":"HSTHHS","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=HSTHHS","meetings":[],
    "members":[
    {"id":"BARLOSE","position":"member"}
    ,{"id":"CHAVER","position":"member"}
    ,{"id":"DAWBM","position":"chair"}
    ,{"id":"HALLHC","position":"member"}
    ,{"id":"HOLLIS","position":"member"}
    ,{"id":"KENNEMS","position":"vice chair"}
    ,{"id":"MILESKB","position":"member"}
    ,{"id":"RAYP","position":"member"}
    ,{"id":"REDDEH","position":"member"}
    ,{"id":"SPENDRM","position":"member"}
    ,{"id":"THURSNK","position":"member"}
    ,{"id":"WARDR","position":"member"}]
    }
    ,{"description":"House Judiciary Committee","id":"HSTJUD","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=HSTJUD","meetings":[],
    "members":[
    {"id":"COLEMK","position":"member"}
    ,{"id":"CUTLEBR","position":"member"}
    ,{"id":"GREENBM","position":"member"}
    ,{"id":"IVORYK","position":"member"}
    ,{"id":"KINGBS","position":"member"}
    ,{"id":"LISONK","position":"member"}
    ,{"id":"MCKELMK","position":"chair"}
    ,{"id":"PITCHDM","position":"member"}
    ,{"id":"PULSIS","position":"member"}
    ,{"id":"QUINNT","position":"member"}
    ,{"id":"SNOWVL","position":"vice chair"}
    ,{"id":"WHEATMA","position":"member"}]
    }
    ,{"description":"House Law Enforcement and Criminal Justice Committee","id":"HSTLAW","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=HSTLAW","meetings":[],
    "members":[
    {"id":"EDWARRP","position":"member"}
    ,{"id":"ELIASS","position":"member"}
    ,{"id":"GARDIA","position":"member"}
    ,{"id":"HOLLIS","position":"member"}
    ,{"id":"HUTCHEK","position":"member"}
    ,{"id":"MILESKB","position":"member"}
    ,{"id":"PERRYLB","position":"chair"}
    ,{"id":"RAYP","position":"member"}
    ,{"id":"REDDEH","position":"vice chair"}
    ,{"id":"ROMERAY","position":"member"}
    ,{"id":"WEIGHE","position":"member"}
    ,{"id":"WINDEM","position":"member"}]
    }
    ,{"description":"House Legislative Expense Oversight Committee","id":"SPEHEO","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEHEO","meetings":[],
    "members":[
    {"id":"HUGHEGH","position":"chair"}
    ,{"id":"KINGBS","position":"member"}
    ,{"id":"WILSOBR","position":"member"}]
    }
    ,{"description":"House Natural Resources, Agriculture, and Environment Committee","id":"HSTNAE","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=HSTNAE","meetings":[],
    "members":[
    {"id":"BARLOSE","position":"vice chair"}
    ,{"id":"BRISCJK","position":"member"}
    ,{"id":"CHEWSH","position":"member"}
    ,{"id":"DUCKWS","position":"member"}
    ,{"id":"HANDYSG","position":"member"}
    ,{"id":"HAWKETD","position":"member"}
    ,{"id":"NOELME","position":"member"}
    ,{"id":"OWENSD","position":"member"}
    ,{"id":"SAGERD","position":"member"}
    ,{"id":"SANDASD","position":"member"}
    ,{"id":"STRATKJ","position":"chair"}
    ,{"id":"WATKICF","position":"member"}
    ,{"id":"WILDEL","position":"member"}]
    }
    ,{"description":"House Political Subdivisions Committee","id":"HSTPOL","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=HSTPOL","meetings":[],
    "members":[
    {"id":"DUNNIJA","position":"member"}
    ,{"id":"GROVEK","position":"member"}
    ,{"id":"HALLHC","position":"vice chair"}
    ,{"id":"KWANK","position":"member"}
    ,{"id":"PITCHDM","position":"chair"}
    ,{"id":"POTTEVK","position":"member"}
    ,{"id":"POULSMH","position":"member"}
    ,{"id":"PULSIS","position":"member"}
    ,{"id":"ROBERMK","position":"member"}
    ,{"id":"WARDR","position":"member"}
    ,{"id":"WEBBRC","position":"member"}
    ,{"id":"WEIGHE","position":"member"}
    ,{"id":"WILDEL","position":"member"}]
    }
    ,{"description":"House Public Utilities, Energy, and Technology Committee","id":"HSTPUT","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=HSTPUT","meetings":[],
    "members":[
    {"id":"ALBRECR","position":"member"}
    ,{"id":"ARENTPM","position":"member"}
    ,{"id":"BROOKW","position":"member"}
    ,{"id":"CHEWSH","position":"member"}
    ,{"id":"CHRISKJ","position":"member"}
    ,{"id":"GROVEK","position":"member"}
    ,{"id":"HANDYSG","position":"chair"}
    ,{"id":"HEMINLN","position":"member"}
    ,{"id":"MALOYC","position":"member"}
    ,{"id":"NELSOMF","position":"vice chair"}
    ,{"id":"STRATKJ","position":"member"}]
    }
    ,{"description":"House Retirement and Independent Entities Committee","id":"HSTRIE","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=HSTRIE","meetings":[],
    "members":[
    {"id":"CHRISFL","position":"chair"}
    ,{"id":"DUCKWS","position":"member"}
    ,{"id":"ELIASS","position":"member"}
    ,{"id":"HAWKETD","position":"vice chair"}
    ,{"id":"HEMINLN","position":"member"}
    ,{"id":"MCCAYD","position":"member"}
    ,{"id":"MOSSJ","position":"member"}
    ,{"id":"PERRYLB","position":"member"}
    ,{"id":"POULSMH","position":"member"}]
    }
    ,{"description":"House Revenue and Taxation Committee","id":"HSTREV","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=HSTREV","meetings":[],
    "members":[
    {"id":"BRISCJK","position":"member"}
    ,{"id":"ELIASS","position":"chair"}
    ,{"id":"FROERG","position":"member"}
    ,{"id":"GREENBM","position":"member"}
    ,{"id":"IVORYK","position":"member"}
    ,{"id":"KINGBS","position":"member"}
    ,{"id":"LISONK","position":"member"}
    ,{"id":"MOSSJ","position":"member"}
    ,{"id":"QUINNT","position":"member"}
    ,{"id":"SAGERD","position":"vice chair"}
    ,{"id":"STANAJE","position":"member"}
    ,{"id":"WILSOBR","position":"member"}]
    }
    ,{"description":"House Rules Committee","id":"HSTRUL","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=HSTRUL","meetings":[],
    "members":[
    {"id":"CHAVER","position":"member"}
    ,{"id":"FAWSOJL","position":"member"}
    ,{"id":"MOSSCS","position":"member"}
    ,{"id":"NOELME","position":"chair"}
    ,{"id":"PETERVL","position":"member"}
    ,{"id":"SCHULM","position":"member"}
    ,{"id":"STANAJE","position":"vice chair"}
    ,{"id":"WATKICF","position":"member"}]
    }
    ,{"description":"House Transportation Committee","id":"HSTTRA","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=HSTTRA","meetings":[],
    "members":[
    {"id":"BROOKW","position":"member"}
    ,{"id":"CHRISKJ","position":"vice chair"}
    ,{"id":"FAWSOJL","position":"member"}
    ,{"id":"HEMINLN","position":"member"}
    ,{"id":"KENNEMS","position":"member"}
    ,{"id":"KNOTWJ","position":"member"}
    ,{"id":"KWANK","position":"member"}
    ,{"id":"MOSSJ","position":"member"}
    ,{"id":"POTTEVK","position":"member"}
    ,{"id":"SCHULM","position":"chair"}
    ,{"id":"SPENDRM","position":"member"}
    ,{"id":"WESTWJR","position":"member"}]
    }
    ,{"description":"Infrastructure and General Government Appropriations Subcommittee","id":"APPIGG","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=APPIGG","meetings":[
    {"mtgTime":"2017-07-20T8:00:00.000Z","mtgPlace":"445 State Capitol","status":"O"}
    ,{"mtgTime":"2017-10-19T8:00:00.000Z","mtgPlace":"445 State Capitol","status":"O"}],
    "members":[
    {"id":"ADAMSJS","position":"member"}
    ,{"id":"ANDERJL","position":"member"}
    ,{"id":"BROOKW","position":"house vice chair"}
    ,{"id":"BUXTODG","position":"member"}
    ,{"id":"FROERG","position":"house chair"}
    ,{"id":"HALLHC","position":"member"}
    ,{"id":"HARPEWA","position":"senate chair"}
    ,{"id":"HEMINLN","position":"member"}
    ,{"id":"HILLYLW","position":"member"}
    ,{"id":"HINKIDP","position":"member"}
    ,{"id":"KNOTWJ","position":"member"}
    ,{"id":"MALOYC","position":"member"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"MCKELMK","position":"member"}
    ,{"id":"PITCHDM","position":"member"}
    ,{"id":"POULSMH","position":"member"}
    ,{"id":"SAGERD","position":"member"}
    ,{"id":"SCHULM","position":"member"}]
    }
    ,{"description":"Judicial Rules Review Committee","id":"SPEJRR","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEJRR","meetings":[],
    "members":[
    {"id":"DAVISG","position":"member"}
    ,{"id":"DUCKWS","position":"member"}
    ,{"id":"HEMMED","position":"member"}
    ,{"id":"HUGHEGH","position":"member"}
    ,{"id":"MCCAYD","position":"chair"}
    ,{"id":"WEILET","position":"chair"}]
    }
    ,{"description":"Legislative Audit Subcommittee","id":"SPEAUD","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEAUD","meetings":[],
    "members":[
    {"id":"DAVISG","position":"member"}
    ,{"id":"HUGHEGH","position":"co-chair"}
    ,{"id":"KINGBS","position":"member"}
    ,{"id":"NIEDEWL","position":"co-chair"}
    ,{"id":"OKERLR","position":"member"}
    ,{"id":"WILSOBR","position":"member"}]
    }
    ,{"description":"Legislative Management Committee","id":"SPEMAN","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEMAN","meetings":[
    {"mtgTime":"2017-04-11T15:00:00.000Z","mtgPlace":"445 State Capitol","status":"O"}],
    "members":[
    {"id":"ADAMSJS","position":"member"}
    ,{"id":"BRISCJK","position":"member"}
    ,{"id":"DAVISG","position":"member"}
    ,{"id":"ESCAML","position":"member"}
    ,{"id":"GIBSOFD","position":"member"}
    ,{"id":"HOLLIS","position":"member"}
    ,{"id":"HUGHEGH","position":"chair"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"KINGBS","position":"member"}
    ,{"id":"KNOTWJ","position":"member"}
    ,{"id":"KNUDSPC","position":"member"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"NIEDEWL","position":"vice chair"}
    ,{"id":"OKERLR","position":"member"}
    ,{"id":"ROMERAY","position":"member"}
    ,{"id":"WILSOBR","position":"member"}]
    }
    ,{"description":"Legislative Process Committee","id":"SPELPC","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPELPC","meetings":[],
    "members":[
    {"id":"ARENTPM","position":"member"}
    ,{"id":"CHAVER","position":"member"}
    ,{"id":"DAVISG","position":"member"}
    ,{"id":"DUNNIJA","position":"chair"}
    ,{"id":"HENDEDM","position":"member"}
    ,{"id":"HILLYLW","position":"chair"}
    ,{"id":"PERRYLB","position":"member"}
    ,{"id":"RAYP","position":"member"}]
    }
    ,{"description":"Natural Resources, Agriculture, and Environmental Quality Appropriations Subcommittee","id":"APPNAE","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=APPNAE","meetings":[
    {"mtgTime":"2017-06-22T8:00:00.000Z","mtgPlace":"210 Senate Building","status":"O"}],
    "members":[
    {"id":"CHEWSH","position":"house vice chair"}
    ,{"id":"CHRISKJ","position":"member"}
    ,{"id":"DABAKJ","position":"member"}
    ,{"id":"DAYTOM","position":"member"}
    ,{"id":"DUCKWS","position":"member"}
    ,{"id":"GREENBM","position":"member"}
    ,{"id":"HANDYSG","position":"member"}
    ,{"id":"HAWKETD","position":"member"}
    ,{"id":"HINKIDP","position":"senate chair"}
    ,{"id":"IPSONDL","position":"member"}
    ,{"id":"IVORYK","position":"house chair"}
    ,{"id":"KNUDSPC","position":"member"}
    ,{"id":"KWANK","position":"member"}
    ,{"id":"NOELME","position":"member"}
    ,{"id":"OKERLR","position":"member"}
    ,{"id":"PERRYLB","position":"member"}
    ,{"id":"ROBERMK","position":"member"}
    ,{"id":"STRATKJ","position":"member"}
    ,{"id":"VICKEEJ","position":"member"}]
    }
    ,{"description":"Occupational and Professional Licensure Review Committee","id":"SPEOPL","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEOPL","meetings":[],
    "members":[
    {"id":"DUCKWS","position":"member"}
    ,{"id":"GREENBM","position":"chair"}
    ,{"id":"HARPEWA","position":"member"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"ROBERMK","position":"member"}
    ,{"id":"WEILET","position":"chair"}]
    }
    ,{"description":"Point of the Mountain Development Commission","id":"SPEPMD","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEPMD","meetings":[
    {"mtgTime":"2017-04-20T13:30:00.000Z","mtgPlace":"445 State Capitol","status":"O"}],
    "members":[
    {"id":"FILLML","position":"member"}
    ,{"id":"SNOWVL","position":"chair"}
    ,{"id":"STEVEJW","position":"member"}
    ,{"id":"WILSOBR","position":"member"}]
    }
    ,{"description":"Public Education Appropriations Subcommittee","id":"APPPED","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=APPPED","meetings":[
    {"mtgTime":"2017-06-22T8:00:00.000Z","mtgPlace":"445 State Capitol","status":"O"}],
    "members":[
    {"id":"ADAMSJS","position":"member"}
    ,{"id":"ARENTPM","position":"member"}
    ,{"id":"BRISCJK","position":"member"}
    ,{"id":"CHRISFL","position":"member"}
    ,{"id":"ELIASS","position":"member"}
    ,{"id":"FAWSOJL","position":"member"}
    ,{"id":"FILLML","position":"member"}
    ,{"id":"GIBSOFD","position":"member"}
    ,{"id":"HILLYLW","position":"senate chair"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"LASTBG","position":"member"}
    ,{"id":"LISONK","position":"member"}
    ,{"id":"MCCAYD","position":"house chair"}
    ,{"id":"MILLNA","position":"member"}
    ,{"id":"MOSSJ","position":"member"}
    ,{"id":"PULSIS","position":"member"}
    ,{"id":"SPENDRM","position":"house vice chair"}
    ,{"id":"STEPHHA","position":"member"}
    ,{"id":"STEVEJW","position":"member"}
    ,{"id":"THATCDW","position":"member"}
    ,{"id":"THURSNK","position":"member"}]
    }
    ,{"description":"Retirement and Independent Entities Appropriations Subcommittee","id":"APPRIE","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=APPRIE","meetings":[],
    "members":[
    {"id":"CHRISFL","position":"house chair"}
    ,{"id":"DAVISG","position":"member"}
    ,{"id":"DUCKWS","position":"member"}
    ,{"id":"ELIASS","position":"member"}
    ,{"id":"FILLML","position":"member"}
    ,{"id":"HARPEWA","position":"member"}
    ,{"id":"HAWKETD","position":"house vice chair"}
    ,{"id":"HEMINLN","position":"member"}
    ,{"id":"HEMMED","position":"senate chair"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"MCCAYD","position":"member"}
    ,{"id":"MOSSJ","position":"member"}
    ,{"id":"PERRYLB","position":"member"}
    ,{"id":"POULSMH","position":"member"}
    ,{"id":"WEILET","position":"member"}]
    }
    ,{"description":"Senate Business and Labor Committee","id":"SSTBUS","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SSTBUS","meetings":[],
    "members":[
    {"id":"BRAMBCS","position":"chair"}
    ,{"id":"DAVISG","position":"member"}
    ,{"id":"HEMMED","position":"member"}
    ,{"id":"IPSONDL","position":"member"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"OKERLR","position":"member"}
    ,{"id":"STEVEJW","position":"member"}
    ,{"id":"WEILET","position":"member"}]
    }
    ,{"description":"Senate Business and Labor Confirmation Committee","id":"SPEBUS","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEBUS","meetings":[],
    "members":[
    {"id":"ANDERJL","position":"member"}
    ,{"id":"BRAMBCS","position":"chair"}
    ,{"id":"BUXTODG","position":"member"}
    ,{"id":"DAVISG","position":"member"}
    ,{"id":"HEMMED","position":"member"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"SHIOZBE","position":"member"}]
    }
    ,{"description":"Senate Economic Development and Workforce Services Committee","id":"SSTEDW","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SSTEDW","meetings":[],
    "members":[
    {"id":"ANDERJL","position":"chair"}
    ,{"id":"BUXTODG","position":"member"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"MILLNA","position":"member"}
    ,{"id":"NIEDEWL","position":"member"}
    ,{"id":"OKERLR","position":"member"}
    ,{"id":"STEVEJW","position":"member"}]
    }
    ,{"description":"Senate Economic Development and Workforce Services Confirmation Committee","id":"SPEEDW","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEEDW","meetings":[],
    "members":[
    {"id":"ANDERJL","position":"member"}
    ,{"id":"BRAMBCS","position":"member"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"MILLNA","position":"member"}
    ,{"id":"SHIOZBE","position":"chair"}
    ,{"id":"STEVEJW","position":"member"}]
    }
    ,{"description":"Senate Education Committee","id":"SSTEDU","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SSTEDU","meetings":[
    ],
    "members":[
    {"id":"ADAMSJS","position":"member"}
    ,{"id":"HENDEDM","position":"member"}
    ,{"id":"HILLYLW","position":"member"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"MILLNA","position":"chair"}
    ,{"id":"NIEDEWL","position":"member"}
    ,{"id":"STEPHHA","position":"member"}
    ]
    }
    ,{"description":"Senate Education Confirmation Committee","id":"SPEEDU","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEEDU","meetings":[],
    "members":[
    {"id":"ADAMSJS","position":"member"}
    ,{"id":"ESCAML","position":"member"}
    ,{"id":"HILLYLW","position":"member"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"MILLNA","position":"member"}
    ,{"id":"STEPHHA","position":"member"}
    ,{"id":"STEVEJW","position":"member"}
    ,{"id":"VICKEEJ","position":"chair"}]
    }
    ,{"description":"Senate Ethics Committee","id":"SSTETH","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SSTETH","meetings":[],
    "members":[
    {"id":"CHRISAM","position":"member"}
    ,{"id":"DAVISG","position":"vice chair"}
    ,{"id":"ESCAML","position":"member"}
    ,{"id":"HENDEDM","position":"member"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"KNUDSPC","position":"chair"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"STEVEJW","position":"member"}]
    }
    ,{"description":"Senate Government Operations and Political Subdivisions Committee","id":"SSTGOP","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SSTGOP","meetings":[],
    "members":[
    {"id":"ADAMSJS","position":"member"}
    ,{"id":"DAYTOM","position":"member"}
    ,{"id":"ESCAML","position":"member"}
    ,{"id":"HINKIDP","position":"member"}
    ,{"id":"IPSONDL","position":"chair"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"KNUDSPC","position":"member"}
    ,{"id":"THATCDW","position":"member"}]
    }
    ,{"description":"Senate Government Operations Confirmation Committee","id":"SPEGOV","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEGOV","meetings":[],
    "members":[
    {"id":"ANDERJL","position":"member"}
    ,{"id":"ESCAML","position":"member"}
    ,{"id":"HARPEWA","position":"chair"}
    ,{"id":"HINKIDP","position":"member"}
    ,{"id":"IPSONDL","position":"member"}
    ,{"id":"KNUDSPC","position":"member"}
    ,{"id":"MAYNEK","position":"member"}]
    }
    ,{"description":"Senate Health and Human Services Committee","id":"SSTHHS","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SSTHHS","meetings":[],
    "members":[
    {"id":"CHRISAM","position":"member"}
    ,{"id":"DABAKJ","position":"member"}
    ,{"id":"ESCAML","position":"member"}
    ,{"id":"FILLML","position":"chair"}
    ,{"id":"KNUDSPC","position":"member"}
    ,{"id":"SHIOZBE","position":"member"}
    ,{"id":"VANTAKT","position":"member"}
    ,{"id":"VICKEEJ","position":"member"}]
    }
    ,{"description":"Senate Health and Human Services Confirmation Committee","id":"SPEHHS","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEHHS","meetings":[],
    "members":[
    {"id":"CHRISAM","position":"chair"}
    ,{"id":"DABAKJ","position":"member"}
    ,{"id":"ESCAML","position":"member"}
    ,{"id":"FILLML","position":"member"}
    ,{"id":"HEMMED","position":"member"}
    ,{"id":"VANTAKT","position":"member"}
    ,{"id":"VICKEEJ","position":"member"}]
    }
    ,{"description":"Senate Judicial Confirmation Committee","id":"SPESJC","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPESJC","meetings":[],
    "members":[
    {"id":"DABAKJ","position":"member"}
    ,{"id":"HILLYLW","position":"member"}
    ,{"id":"KNUDSPC","position":"member"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"SHIOZBE","position":"member"}
    ,{"id":"VANTAKT","position":"member"}
    ,{"id":"WEILET","position":"chair"}]
    }
    ,{"description":"Senate Judiciary Confirmation Committee","id":"SPEJUD","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEJUD","meetings":[],
    "members":[
    {"id":"ESCAML","position":"member"}
    ,{"id":"FILLML","position":"member"}
    ,{"id":"HILLYLW","position":"chair"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"KNUDSPC","position":"member"}
    ,{"id":"THATCDW","position":"member"}
    ,{"id":"WEILET","position":"member"}]
    }
    ,{"description":"Senate Judiciary, Law Enforcement, and Criminal Justice Committee","id":"SSTJLC","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SSTJLC","meetings":[],
    "members":[
    {"id":"DAVISG","position":"member"}
    ,{"id":"ESCAML","position":"member"}
    ,{"id":"HILLYLW","position":"member"}
    ,{"id":"NIEDEWL","position":"member"}
    ,{"id":"OKERLR","position":"member"}
    ,{"id":"THATCDW","position":"member"}
    ,{"id":"WEILET","position":"chair"}]
    }
    ,{"description":"Senate Law Enforcement and Criminal Justice Confirmation Committee","id":"SPELEC","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPELEC","meetings":[],
    "members":[
    {"id":"DAVISG","position":"member"}
    ,{"id":"IPSONDL","position":"member"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"OKERLR","position":"member"}
    ,{"id":"THATCDW","position":"chair"}
    ,{"id":"VANTAKT","position":"member"}
    ,{"id":"WEILET","position":"member"}]
    }
    ,{"description":"Senate Natural Resources, Agriculture, and Environment Committee","id":"SSTNAE","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SSTNAE","meetings":[],
    "members":[
    {"id":"CHRISAM","position":"member"}
    ,{"id":"DAYTOM","position":"chair"}
    ,{"id":"HINKIDP","position":"member"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"KNUDSPC","position":"member"}
    ,{"id":"SHIOZBE","position":"member"}
    ,{"id":"VICKEEJ","position":"member"}]
    }
    ,{"description":"Senate Natural Resources, Agriculture, and Environment Confirmation Committee","id":"SPENAT","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPENAT","meetings":[],
    "members":[
    {"id":"CHRISAM","position":"member"}
    ,{"id":"DABAKJ","position":"member"}
    ,{"id":"DAYTOM","position":"chair"}
    ,{"id":"HINKIDP","position":"member"}
    ,{"id":"IPSONDL","position":"member"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"OKERLR","position":"member"}
    ,{"id":"VICKEEJ","position":"member"}]
    }
    ,{"description":"Senate Political Subdivisions Confirmation Committee","id":"SPEPOL","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEPOL","meetings":[],
    "members":[
    {"id":"BUXTODG","position":"member"}
    ,{"id":"DABAKJ","position":"member"}
    ,{"id":"DAYTOM","position":"member"}
    ,{"id":"ESCAML","position":"member"}
    ,{"id":"HARPEWA","position":"member"}
    ,{"id":"IPSONDL","position":"chair"}
    ,{"id":"THATCDW","position":"member"}]
    }
    ,{"description":"Senate Retirement and Independent Entities Committee","id":"SSTRIE","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SSTRIE","meetings":[],
    "members":[
    {"id":"DAVISG","position":"member"}
    ,{"id":"FILLML","position":"member"}
    ,{"id":"HARPEWA","position":"member"}
    ,{"id":"HEMMED","position":"chair"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"WEILET","position":"member"}]
    }
    ,{"description":"Senate Retirement and Independent Entities Confirmation Committee","id":"SPERET","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPERET","meetings":[],
    "members":[
    {"id":"DAVISG","position":"member"}
    ,{"id":"FILLML","position":"member"}
    ,{"id":"HARPEWA","position":"member"}
    ,{"id":"HEMMED","position":"chair"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"WEILET","position":"member"}]
    }
    ,{"description":"Senate Revenue and Taxation Committee","id":"SSTREV","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SSTREV","meetings":[],
    "members":[
    {"id":"BRAMBCS","position":"member"}
    ,{"id":"DABAKJ","position":"member"}
    ,{"id":"DAVISG","position":"member"}
    ,{"id":"FILLML","position":"member"}
    ,{"id":"HARPEWA","position":"member"}
    ,{"id":"HEMMED","position":"member"}
    ,{"id":"HENDEDM","position":"member"}
    ,{"id":"STEPHHA","position":"chair"}]
    }
    ,{"description":"Senate Revenue and Taxation Confirmation Committee","id":"SPEREV","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEREV","meetings":[],
    "members":[
    {"id":"BRAMBCS","position":"member"}
    ,{"id":"DABAKJ","position":"member"}
    ,{"id":"DAVISG","position":"member"}
    ,{"id":"HEMMED","position":"member"}
    ,{"id":"HENDEDM","position":"member"}
    ,{"id":"SHIOZBE","position":"member"}
    ,{"id":"STEPHHA","position":"chair"}]
    }
    ,{"description":"Senate Rules Committee","id":"SSTRUL","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SSTRUL","meetings":[],
    "members":[
    {"id":"HARPEWA","position":"member"}
    ,{"id":"HEMMED","position":"vice chair"}
    ,{"id":"HENDEDM","position":"chair"}
    ,{"id":"HINKIDP","position":"member"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"MILLNA","position":"member"}
    ,{"id":"VICKEEJ","position":"member"}
    ,{"id":"WEILET","position":"member"}]
    }
    ,{"description":"Senate Transportation, Public Utilities, Energy, and Technology Committee","id":"SSTTPT","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SSTTPT","meetings":[],
    "members":[
    {"id":"ADAMSJS","position":"member"}
    ,{"id":"ANDERJL","position":"member"}
    ,{"id":"BUXTODG","position":"chair"}
    ,{"id":"DABAKJ","position":"member"}
    ,{"id":"HARPEWA","position":"member"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"VANTAKT","position":"member"}]
    }
    ,{"description":"Senate Transportation, Public Utilities, Energy, and Technology Confirmation Committee","id":"SPETRA","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPETRA","meetings":[],
    "members":[
    {"id":"ADAMSJS","position":"member"}
    ,{"id":"BUXTODG","position":"chair"}
    ,{"id":"DAVISG","position":"member"}
    ,{"id":"HARPEWA","position":"member"}
    ,{"id":"HENDEDM","position":"member"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"SHIOZBE","position":"member"}
    ,{"id":"VANTAKT","position":"member"}]
    }
    ,{"description":"Social Services Appropriations Subcommittee","id":"APPSOC","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=APPSOC","meetings":[
    {"mtgTime":"2017-06-22T7:59:00.000Z","mtgPlace":"30 House Building","status":"O"}
    ,{"mtgTime":"2017-07-20T7:59:00.000Z","mtgPlace":"30 House Building","status":"O"}
    ,{"mtgTime":"2017-09-18T7:59:00.000Z","mtgPlace":"30 House Building","status":"O"}
    ,{"mtgTime":"2017-10-19T7:59:00.000Z","mtgPlace":"30 House Building","status":"O"}],
    "members":[
    {"id":"ALBRECR","position":"member"}
    ,{"id":"CHAVER","position":"member"}
    ,{"id":"CHRISAM","position":"senate chair"}
    ,{"id":"EDWARRP","position":"member"}
    ,{"id":"ESCAML","position":"member"}
    ,{"id":"HEMMED","position":"member"}
    ,{"id":"HOLLIS","position":"member"}
    ,{"id":"KENNEMS","position":"member"}
    ,{"id":"NIEDEWL","position":"member"}
    ,{"id":"RAYP","position":"house chair"}
    ,{"id":"REDDEH","position":"member"}
    ,{"id":"SHIOZBE","position":"member"}
    ,{"id":"VANTAKT","position":"member"}
    ,{"id":"WARDR","position":"house vice chair"}
    ,{"id":"WATKICF","position":"member"}
    ,{"id":"WEILET","position":"member"}]
    }
    ,{"description":"State Water Development Commission","id":"SPESWD","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPESWD","meetings":[],
    "members":[
    {"id":"ALBRECR","position":"member"}
    ,{"id":"BRISCJK","position":"member"}
    ,{"id":"CHEWSH","position":"member"}
    ,{"id":"DAYTOM","position":"chair"}
    ,{"id":"DUCKWS","position":"member"}
    ,{"id":"FROERG","position":"member"}
    ,{"id":"GROVEK","position":"chair"}
    ,{"id":"HINKIDP","position":"member"}
    ,{"id":"IPSONDL","position":"member"}
    ,{"id":"IWAMOJ","position":"member"}
    ,{"id":"NOELME","position":"member"}
    ,{"id":"SNOWVL","position":"member"}
    ,{"id":"VANTAKT","position":"member"}]
    }
    ,{"description":"Subcommittee on Oversight","id":"SUBOVE","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SUBOVE","meetings":[],
    "members":[
    {"id":"BRISCJK","position":"member"}
    ,{"id":"DAVISG","position":"member"}
    ,{"id":"HUGHEGH","position":"chair"}
    ,{"id":"KINGBS","position":"member"}
    ,{"id":"MAYNEK","position":"member"}
    ,{"id":"NIEDEWL","position":"member"}
    ,{"id":"OKERLR","position":"member"}
    ,{"id":"WILSOBR","position":"member"}]
    }
    ,{"description":"Utah International Relations and Trade Commission","id":"SPEUIR","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPEUIR","meetings":[],
    "members":[
    {"id":"ANDERJL","position":"member"}
    ,{"id":"ARENTPM","position":"member"}
    ,{"id":"BRAMBCS","position":"chair"}
    ,{"id":"DAVISG","position":"member"}
    ,{"id":"GROVEK","position":"member"}
    ,{"id":"HEMINLN","position":"member"}
    ,{"id":"HUTCHEK","position":"chair"}
    ,{"id":"SPENDRM","position":"member"}]
    }
    ,{"description":"Utah Tax Review Commission","id":"SPETAX","link":"http://le.utah.gov/asp/interim/Commit.asp?Year=2017&Com=SPETAX","meetings":[],
    "members":[
    {"id":"BRISCJK","position":"member"}
    ,{"id":"DABAKJ","position":"member"}
    ,{"id":"ELIASS","position":"member"}
    ,{"id":"HILLYLW","position":"member"}
    ,{"id":"MCCAYD","position":"member"}
    ,{"id":"STEPHHA","position":"chair"}]
    }
    ]


    for committee in committees_info:
        committee_name = committee["description"]
        r = urllib.urlopen(committee["link"]).read()
        soup = BeautifulSoup(r)
        letters = soup.find_all("div", id="overview")
        prefix = "http://le.utah.gov/asp/roster/"
        overview = letters[0].text.encode('ascii', 'replace').replace(u'\u2022', '()').replace(u'\u201c', ' ').replace(u'\u201d', ' ').replace(u'\u2019', ' ')

        # overview = overview.replace(u'\u201c', ' ').replace(u'\u201d', ' ').replace(u'\u2019', ' ')
        print overview
        committee_id = mysql_committee_entry.main(committee_name, str(overview))
        for member in committee["members"]:
            member_id = member["id"]
            position = member["position"]
            mysql_committee_person_entry.main(member_id, committee_id, str(position))



if __name__ == "__main__":

    # if len(sys.argv) != 1:
    #     print "Usage: python grabber_ksl.py [ current_time ]"
    # else:
    #     currentTime = []
    #     currentTime.append((time.strftime("%x").replace("/", " ")).split())
    #     currentTime.append((time.strftime("%X").replace(":", " ")).split())
    main()
