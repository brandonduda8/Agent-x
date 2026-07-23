from genesis_opportunity_execution_engine import opportunity_engine


items = [

("jobs",
"Indeed",
"Remote customer support position",
"immediate remote income opportunity"),

("jobs",
"LinkedIn",
"Technical support specialist",
"remote income opportunity"),

("contracts",
"Upwork",
"AI automation assistant project",
"immediate income opportunity"),

("business_leads",
"Google Business",
"Dental clinic AI receptionist prospect",
"business revenue opportunity"),

("housing",
"Resource Database",
"Rental assistance program",
"immediate housing support")

]


for item in items:
    print(
        opportunity_engine.add_opportunity(
            item[0],
            item[1],
            item[2],
            item[3]
        )
    )


print(opportunity_engine.status())
