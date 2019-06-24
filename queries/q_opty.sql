SELECT Account.Industry_Vertical__c, Account.Name, Account.of_Active_Opps__c, Account.of_Opps_Created_Last_30_Days__c, Account.of_Opps_Created_this_Calendar_Year__c, Account.X18_Digit_ID__c 
FROM Contact 
WHERE (Account.of_Active_Opps__c > 0 
	OR Account.of_Opps_Created_Last_30_Days__c > 0 
	OR Account.of_Opps_Created_this_Calendar_Year__c > 0) 
	AND X18_Digit_Contact_ID__c in (