# Scrape Pardot extracted emails for leads and contact id's for opportunities
# ----------------------------------------------------------------------------
import io
import sys
import os
from os.path import expanduser as ospath
import numpy as np
import pandas as pd
import xlsxwriter
from collections import OrderedDict
from simple_salesforce import Salesforce
import pytz
import datetime
from simple_salesforce import Salesforce
from salesforce_reporting import Connection, ReportParser
with open('~/.sfdc') as f:                                                       # read in authentication params
    uname, spass, stoken, ppass, ptoken = [x.strip("\n") for x in f.readlines()]

soql_opty = "queries/q_opty.sql"                                                 # stored query
soql_lead = "queries/q_lead.sql"                                                 # stored query
excel_path = "~/Four Winds Interactive/Marketing - Documents/s_data/"            # directory - case sensistve
excel_file = "pardot.xlsx"                                                       # excel file - case sensistve
sheet_id_opty = "id_opty"                                                        # sheet - case sensistve
sheet_id_lead = "email_lead"                                                     # sheet - case sensistve

sf = Salesforce(username=uname, password=spass, security_token=stoken)           # authenticate
end = datetime.datetime.now(pytz.UTC)                                            # salesforce API requires UTC
print("@ ", end)

with open(soql_opty, 'r') as file:                                # get opty soql query from file
    soql_opty = file.read().replace('\n','')                      # remove line breaks
    soql_opty = soql_opty.replace('\t','')                        # remove tabs
opty_id = pd.read_excel(excel_path + excel_file, sheet_id_opty)   # read ids from excel file
opty_id = tuple(list(opty_id['x18ContactID']))                    # convert dataframe column to list then tuple
opty_id = "','".join(opty_id)                                     # convert tuple to comma sep string
soql_opty = soql_opty + "'" + opty_id + "')"
q_opty = sf.query(soql_opty)
records = [dict(
      IndVert=rec['Account']['Industry_Vertical__c'],
         Name=rec['Account']['Name'],
     optysAct=rec['Account']['of_Active_Opps__c'],
     optyss30=rec['Account']['of_Opps_Created_Last_30_Days__c'],
     optyssYr=rec['Account']['of_Opps_Created_this_Calendar_Year__c'],
     x18actid=rec['Account']['X18_Digit_ID__c']) 
    for rec in q_opty['records']]
df_opty = pd.DataFrame(records)
df_opty.to_csv(excel_path + 'p_opty.csv')

with open(soql_lead, 'r') as file:                                 # get lead soql query from file
    soql_lead = file.read().replace('\n','')                       # remove line breaks
    soql_lead = soql_lead.replace('\t','')                         # remove tabs
lead_email = pd.read_excel(excel_path + excel_file, sheet_id_lead) # read ids from excel file
lead_email = tuple(list(lead_email['Email']))                      # dataframe column to list to tuple
lead_email = "','".join(lead_email)                                # tuple to comma sep string
soql_lead = soql_lead + "'" + lead_email + "')"
q_lead = sf.query(soql_lead)
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
df_lead = pd.DataFrame(records)
df_lead.to_csv(excel_path + 'p_lead.csv')
