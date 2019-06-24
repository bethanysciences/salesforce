#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), '../jupyter'))
	print(os.getcwd())
except:
	pass

#%%
# ----------------------------------------------------------------------------- #
# Match Pardot campaign results to new related leads or opportunities           #
#     1) match engaged 18-digit contact IDs to related account opportunities    #
#     2) match engaged email adddresses to generated leads                      #
#                                                                               #
# Bobby Smith 2019 MIT License github www.bethanyscienes.net                    #
# ----------------------------------------------------------------------------- #

# Package instantiations ------------------------------------------------------ #

import io
import sys
import os
from os.path import expanduser as ospath
import numpy as np
import pandas as pd
from collections import OrderedDict           # decode salesforce soql returns
import pytz
import datetime

  # salesforce rest api https://github.com/simple-salesforce/simple-salesforce
from simple_salesforce import Salesforce       # pip3 install simple-salesforce
import xlrd                                    # pip3 install xlrd

# Set IO files and paths ------------------------------------------------------ #

   # path to excel contact id / email supply and outputs files (case sensistve)
excel_path = "~/Four Winds Interactive/Marketing - Documents/s_data/"  
excel_file = "pardot.xlsx"                                  # excel source file

# Authenticate to Salesforce -------------------------------------------------- #
# file format of '.sfdc' (in home directory)
#   salesforce / pardot username (email)
#   salesforce password
#   salesforce API token (changes on each password change)

passfile = os.path.expanduser(os.path.join("~/", ".sfdc"))   # credentials file
with open(passfile) as f:                       # read in authentication params
    uname, spass, stoken, ppass, ptoken = [x.strip("\n") for x in f.readlines()]
    
sf = Salesforce(username=uname,                              # authenticate
                password=spass, 
                security_token=stoken)      

end = datetime.datetime.now(pytz.UTC)           # salesforce API requires UTC
print("@ ", end)

# Process for opportunities --------------------------------------------------- #

# stored query text files use sql extension for linting in editors like vscode
soql_opty = "queries/q_opty.sql"

# referenced worksheet with list of contact ids to query (case sensitive)
sheet_id_opty = "id_opty"
with open(soql_opty, 'r') as file:                                  # open file
    soql_opty = file.read().replace('\n','')               # remove line breaks
    soql_opty = soql_opty.replace('\t','')                        # remove tabs

# read id column into pandas dataframe
opty_id = pd.read_excel(excel_path + excel_file, sheet_id_opty)   
opty_id = tuple(list(opty_id['x18ContactID']))     # dataframe to list to tuple
opty_id = "','".join(opty_id)                       # tuple to comma sep string

soql_opty = soql_opty + "'" + opty_id + "')"                 # build soql query
q_opty = sf.query(soql_opty)                 # submit query to simplesalesforce

# process returned dictionary - fields very by salesforce domain
records = [dict(                                  
      IndVert=rec['Account']['Industry_Vertical__c'],          
         Name=rec['Account']['Name'],
     optysAct=rec['Account']['of_Active_Opps__c'],
     optyss30=rec['Account']['of_Opps_Created_Last_30_Days__c'],
     optyssYr=rec['Account']['of_Opps_Created_this_Calendar_Year__c'],
     x18actid=rec['Account']['X18_Digit_ID__c']) 
    for rec in q_opty['records']]

df_opty = pd.DataFrame(records)                   # output results as dataframe
df_opty.to_csv(excel_path + 'p_opty.csv')       # convert dataframe to csv file

# Process for leads ----------------------------------------------------------- #

# stored query text files use sql extension for linting in editors like vscode
soql_lead = "queries/q_lead.sql"
sheet_id_lead = "email_lead"
with open(soql_lead, 'r') as file:                                  # open file
    soql_lead = file.read().replace('\n','')               # remove line breaks
    soql_lead = soql_lead.replace('\t','')                        # remove tabs

# read id column into pandas dataframe
lead_email = pd.read_excel(excel_path + excel_file, sheet_id_lead)
lead_email = tuple(list(lead_email['Email']))      # dataframe to list to tuple
lead_email = "','".join(lead_email)                 # tuple to comma sep string

soql_lead = soql_lead + "'" + lead_email + "')"              # build soql query
q_lead = sf.query(soql_lead)                 # submit query to simplesalesforce

# process returned dictionary - fields very by salesforce domain
records = [dict(
           IndustryVertical=rec['Industry_Vertical__c'],
                      Email=rec['Email'],
                 LeadSource=rec['LeadSource'],
                    Company=rec['Company'],
                CreatedDate=rec['CreatedDate'],
                   LeadType=rec['Lead_Type__c'],
          UnqualifiedReason=rec['Unqualified_Reason__c'],
                         Id=rec['Id'],
         ConvertedAccountId=rec['ConvertedAccountId'],
     ConvertedOpportunityId=rec['ConvertedOpportunityId'],
         ConvertedContactId=rec['ConvertedContactId'])
    for rec in q_lead['records']]

df_lead = pd.DataFrame(records)                   # output results as dataframe
df_lead.to_csv(excel_path + 'p_lead.csv')         # convert dataframe to csv file


#%%
