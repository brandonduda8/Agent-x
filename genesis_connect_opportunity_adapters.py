from core.genesis.genesis_opportunity_adapter_fabric import opportunity_adapter_fabric


adapters = [

    ("LinkedIn Adapter", "jobs", "professional_network"),
    ("Indeed Adapter", "jobs", "job_search"),
    ("ZipRecruiter Adapter", "jobs", "job_search"),
    ("Glassdoor Adapter", "jobs", "job_search"),
    ("USAJobs Adapter", "jobs", "government_jobs"),

    ("Upwork Adapter", "contracts", "freelance_marketplace"),
    ("Fiverr Adapter", "contracts", "service_marketplace"),

    ("Google Business Adapter", "business_leads", "business_directory"),
    ("Dental Clinic Lead Adapter", "business_leads", "healthcare_directory"),

    ("Housing Resource Adapter", "housing", "assistance_database")

]


for adapter in adapters:
    opportunity_adapter_fabric.register(
        adapter[0],
        adapter[1],
        adapter[2]
    )


print(opportunity_adapter_fabric.status())
