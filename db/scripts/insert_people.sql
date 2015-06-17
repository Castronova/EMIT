-------------------------
-- create Organization --
-------------------------

insert into Organizations (OrganizationTypeCV, OrganizationCode, OrganizationName, ParentOrganizationID)
values ('University','usu', 'utah state university', null);

insert into Organizations (OrganizationTypeCV, OrganizationCode, OrganizationName, OrganizationDescription, ParentOrganizationID)
values ('University','uwrl','utah water research laboratory', 'research laboratory Affiliated with utah state university',
coalesce((select min(OrganizationID) from Organizations),1));


-------------------
-- create Person --
-------------------
insert into People (PersonFirstName, PersonLastName)
values ('tony', 'castronova');

insert into People (PersonFirstName, PersonLastName)
values ('francisco', 'arrieta');

insert into People (PersonFirstName, PersonLastName)
values ('michael', 'gallagher');

insert into People (PersonFirstName, PersonLastName)
values ('mario', 'harper');

------------------------
-- create Affiliation --
------------------------
insert into Affiliations (PersonID, OrganizationID, IsPrimaryOrganizationContact, AffiliationStartDate, PrimaryPhone, PrimaryEmail, PrimaryAddress)
values ((select PersonID from People where PersonLastName = 'castronova'),
	(select OrganizationID from Organizations where OrganizationCode = 'uwrl'),
	'false','2014-03-10','435-797-0852','tony.castronova@usu.edu','8200 old main, logan ut, 84322');


--------------------------------------
-- Create simulation Variable in CV --
--------------------------------------
insert  into CV_VariableName (Term, Name, Definition)
values ('simulation','Simulation','Model Simulation Run');
