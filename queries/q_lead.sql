SELECT Industry_Vertical__c, Email, LeadSource, Company, CreatedDate, Lead_Type__c, Unqualified_Reason__c, Id, ConvertedAccountId, ConvertedOpportunityId, ConvertedContactId 
FROM Lead 
WHERE CreatedDate > 2019-03-01T00:00:00.000Z 
	AND Email in (