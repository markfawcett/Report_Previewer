
# The following file paths are check on start-up as they
# are required for the application to run
REQUIRED = {
    # 'templates_dir': 'script_resources/templates-to-copy',
    # 'shell': 'script_resources/templates-to-use/shell.html',
    # 'print_shell': 'script_resources/templates-to-use/printShell.html',
    # 'pastRepText': 'script_resources/templates-to-use/pastRepText.html',
    # 'witnessText': 'script_resources/templates-to-use/witnessText.html',
    # 'writEvText': 'script_resources/templates-to-use/writEvText.html',
    'templates_dir': 'data',
    'shell': 'templates-to-use/shell.html',
    'print_shell': 'templates-to-use/printShell.html',
    'pastRepText': 'templates-to-use/pastRepText.html',
    'witnessText': 'templates-to-use/witnessText.html',
    'writEvText': 'templates-to-use/writEvText.html',
}

# output file names
REPORT        = 'report.html'
SUMMARY       = 'summary.html'
REPORT_PRINT  = 'report_print.html'
SUMMARY_PRINT = 'summary_print.html'

SOURCES = ['ID', 'Word']

REPORT_TYPES = ['Report', 'Special Report']

ROPORT_NUMS = [
    "First", "Second", "Third", "Fourth", "Fifth",
    "Sixth", "Seventh", "Eighth", "Ninth", "Tenth",
    "Eleventh", "Twelfth", "Thirteenth", "Fourteenth", "Fifteenth",
    "Sixteenth", "Seventeenth", "Eighteenth", "Nineteenth", "Twentieth",
    "Twenty-first", "Twenty-second", "Twenty-third", "Twenty-fourth", "Twenty-fifth",
    "Twenty-sixth", "Twenty-seventh", "Twenty-eighth", "Twenty-ninth", "Thirtieth",
    "Thirty-first", "Thirty-second", "Thirty-third", "Thirty-fourth", "Thirty-fifth",
    "Thirty-sixth", "Thirty-seventh", "Thirty-eighth", "Thirty-ninth", "Fortieth",
    "Forty-first", "Forty-second", "Forty-third", "Forty-fourth", "Forty-fifth",
    "Forty-sixth", "Forty-seventh", "Forty-eighth", "Forty-ninth", "Fiftieth",
    "Fifty-first", "Fifty-second", "Fifty-third", "Fifty-fourth", "Fifty-fifth",
    "Fifty-sixth", "Fifty-seventh", "Fifty-eighth", "Fifty-ninth", "Sixtieth",
    "Sixty-first", "Sixty-second", "Sixty-third", "Sixty-fourth", "Sixty-fifth",
    "Sixty-sixth", "Sixty-seventh", "Sixty-eighth", "Sixty-ninth", "Seventieth",
    "Seventy-first", "Seventy-second", "Seventy-third", "Seventy-fourth", "Seventy-fifth",
    "Seventy-sixth", "Seventy-seventh", "Seventy-eighth", "Seventy-ninth", "Eightieth",
    "Seventy-sixth", "Seventy-seventh", "Seventy-eighth", "Seventy-ninth", "Eightieth",
    "Eighty-first", "Eighty-second", "Eighty-third", "Eighty-fourth", "Eighty-fifth",
    "Eighty-sixth", "Eighty-seventh", "Eighty-eighth", "Eighty-ninth", "Ninetieth",
    "Ninety-first", "Ninety-second", "Ninety-third", "Ninety-fourth", "Ninety-fifth",
    "Ninety-sixth", "Ninety-seventh", "Ninety-eighth", "Ninety-ninth", "One hundredth"
]

COMMITTEES_AND_ADDRESSES = {
    "Administration Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/administration-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/administration-committee/publications/"],
    "Backbench Business Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/backbench-business-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/backbench-business-committee/publications/"],
    "Business, Energy and Industrial Strategy Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/business-energy-industrial-strategy/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/business-energy-industrial-strategy/publications/"],
    "Committee of Privileges": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/privileges/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/privileges/publications/"],
    "Committee on Standards": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/standards/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/standards/publications/"],
    "Committees on Arms Export Controls": ["https://www.parliament.uk/business/committees/committees-a-z/other-committees/committee-on-arms-export-controls/", "https://www.parliament.uk/business/committees/committees-a-z/other-committees/committee-on-arms-export-controls/publications/"],
    "Commons Reference Group on Representation and Inclusion": ["https://www.parliament.uk/business/committees/committees-a-z/other-committees/reference-group-representation-inclusion/", "https://www.parliament.uk/business/committees/committees-a-z/other-committees/reference-group-representation-inclusion/publications/"],
    "Consolidation Bills": ["https://www.parliament.uk/business/committees/committees-a-z/joint-select/consolidation-committee/", "https://www.parliament.uk/business/committees/committees-a-z/joint-select/consolidation-committee/publications/"],
    "Defence Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/defence-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/defence-committee/publications/"],
    "Defence Sub-Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/defence-committee/defencesubcommittee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/defence-committee/defencesubcommittee/publications/"],
    "Digital, Culture, Media and Sport Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/digital-culture-media-and-sport-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/digital-culture-media-and-sport-committee/publications/"],
    "Ecclesiastical Committee": ["https://www.parliament.uk/business/committees/committees-a-z/other-committees/ecclesiastical-committee/", "https://www.parliament.uk/business/committees/committees-a-z/other-committees/ecclesiastical-committee/publications/"],
    "Education Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/education-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/education-committee/publications/"],
    "Environment, Food and Rural Affairs Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/environment-food-and-rural-affairs-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/environment-food-and-rural-affairs-committee/publications/"],
    "Environmental Audit Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/environmental-audit-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/environmental-audit-committee/publications/"],
    "European Scrutiny Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/european-scrutiny-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/european-scrutiny-committee/publications/"],
    "European Statutory Instruments Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/european-statutory-instruments/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/european-statutory-instruments/publications/"],
    "Exiting the European Union Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/exiting-the-european-union-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/exiting-the-european-union-committee/publications/"],
    "Finance Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/finance-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/finance-committee/publications/"],
    "Health and Social Care Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/health-and-social-care-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/health-committee/publications/"],
    "High Speed Rail (West Midlands – Crewe) Bill Select Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/high-speed-rail-west-midlands-crewe-bill-select-committee-commons/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/high-speed-rail-west-midlands-crewe-bill-select-committee-commons/publications-17-19/"],
    "Home Affairs Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/home-affairs-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/home-affairs-committee/publications/"],
    "House of Commons Commission": ["https://www.parliament.uk/business/committees/committees-a-z/other-committees/house-of-commons-commission/", "https://www.parliament.uk/business/committees/committees-a-z/other-committees/house-of-commons-commission/publications/"],
    "House of Commons Estimate Audit Committees": ["https://www.parliament.uk/business/committees/committees-a-z/other-committees/estimate-audit-committees/", "https://www.parliament.uk/business/committees/committees-a-z/other-committees/estimate-audit-committees/publications/"],
    "House of Lords Audit Committee": ["https://www.parliament.uk/business/committees/committees-a-z/other-committees/house-of-lords-audit/", "https://www.parliament.uk/business/committees/committees-a-z/other-committees/house-of-lords-audit/publications1/"],
    "Housing, Communities and Local Government Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/housing-communities-and-local-government-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/housing-communities-and-local-government-committee/publications/"],
    "International Development Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/international-development-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/international-development-committee/publications/"],
    "International Trade Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/international-trade-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/international-trade-committee/publications/"],
    "Joint Committee on Human Rights": ["https://www.parliament.uk/business/committees/committees-a-z/joint-select/human-rights-committee/", "https://www.parliament.uk/business/committees/committees-a-z/joint-select/human-rights-committee/publications/"],
    "Joint Committee on Statutory Instruments": ["https://www.parliament.uk/business/committees/committees-a-z/joint-select/statutory-instruments/", "https://www.parliament.uk/business/committees/committees-a-z/joint-select/statutory-instruments/publications/"],
    "Joint Committee on the Draft Domestic Abuse Bill": ["https://www.parliament.uk/business/committees/committees-a-z/joint-select/draft-domestic-abuse-bill/", "https://www.parliament.uk/business/committees/committees-a-z/joint-select/draft-domestic-abuse-bill/ddab-17-19/publications/"],
    "Joint Committee on the Draft Parliamentary Buildings Bill": ["https://www.parliament.uk/business/committees/committees-a-z/joint-select/draft-parliamentary-buildings-bill/", "https://www.parliament.uk/business/committees/committees-a-z/joint-select/draft-parliamentary-buildings-bill/dppb-17-19/publications/"],
    "Joint Committee on the Draft Registration of Overseas Entities Bill": ["https://www.parliament.uk/business/committees/committees-a-z/joint-select/draft-registration-of-overseas-entities-bill/", "https://www.parliament.uk/business/committees/committees-a-z/joint-select/draft-registration-of-overseas-entities-bill/publications/inquiry-page/publications/"],
    "Joint Committee on the National Security Strategy": ["https://www.parliament.uk/business/committees/committees-a-z/joint-select/national-security-strategy/", "https://www.parliament.uk/business/committees/committees-a-z/joint-select/national-security-strategy/publications/"],
    "Justice Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/justice-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/justice-committee/publications/"],
    "Leader's Group on Governance in the House of Lords": ["https://www.parliament.uk/business/committees/committees-a-z/other-committees/leaders-group-governance/", "https://www.parliament.uk/business/committees/committees-a-z/other-committees/leaders-group-governance/publications/"],
    "Liaison Committee (Commons)": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/liaison-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/liaison-committee/publications/"],
    "Liaison Sub-Committee on the effectiveness and influence of the select committee system": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/liaison-committee/liaison-sub-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/liaison-committee/liaison-sub-committee/publications/"],
    "Lord Speaker's Advisory Panel on Works of Art": ["https://www.parliament.uk/business/committees/committees-a-z/other-committees/lords-works-of-art/", "https://www.parliament.uk/business/committees/committees-a-z/other-committees/lords-works-of-art/publications/"],
    "Lord Speaker's committee on the size of the House": ["https://www.parliament.uk/business/committees/committees-a-z/other-committees/size-of-house-committee/", "https://www.parliament.uk/business/committees/committees-a-z/other-committees/size-of-house-committee/publications/"],
    "Members Estimate Committee": ["https://www.parliament.uk/business/committees/committees-a-z/other-committees/members-estimate/", "https://www.parliament.uk/business/committees/committees-a-z/other-committees/members-estimate/publications/"],
    "Members' Expenses Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/members-expenses/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/members-expenses/publications/"],
    "Northern Ireland Affairs Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/northern-ireland-affairs-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/northern-ireland-affairs-committee/publications/"],
    "Petitions Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/petitions-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/petitions-committee/publications/"],
    "Procedure Committee (Commons)": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/procedure-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/procedure-committee/publications/"],
    "Public Accounts Commission": ["https://www.parliament.uk/business/committees/committees-a-z/other-committees/public-accounts-commission/", "https://www.parliament.uk/business/committees/committees-a-z/other-committees/public-accounts-commission/publications/"],
    "Public Accounts Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/public-accounts-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/public-accounts-committee/publications/"],
    "Public Administration and Constitutional Affairs Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/public-administration-and-constitutional-affairs-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/public-administration-and-constitutional-affairs-committee/publications/"],
    "Regulatory Reform Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/regulatory-reform-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/regulatory-reform-committee/publications/"],
    "Science and Technology Committee (Commons)": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/science-and-technology-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/science-and-technology-committee/publications/"],
    "Scottish Affairs Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/scottish-affairs-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/scottish-affairs-committee/publications/"],
    "Speaker's Advisory Committee on Works of Art": ["https://www.parliament.uk/business/committees/committees-a-z/other-committees/works-of-art/", "https://www.parliament.uk/business/committees/committees-a-z/other-committees/works-of-art/publications/"],
    "Speaker's Committee for the Independent Parliamentary Standards Authority (IPSA)": ["https://www.parliament.uk/business/committees/committees-a-z/other-committees/speakers-committee-for-the-independent-parliamentary-standards-authority/", "https://www.parliament.uk/business/committees/committees-a-z/other-committees/speakers-committee-for-the-independent-parliamentary-standards-authority/publications/"],
    "Speaker's Committee on the Electoral Commission": ["https://www.parliament.uk/business/committees/committees-a-z/other-committees/speakers-committee-on-the-electoral-commission/", "https://www.parliament.uk/business/committees/committees-a-z/other-committees/speakers-committee-on-the-electoral-commission/publications/"],
    "Standing Orders (Private Bills) Committee (Commons)": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/standing-orders/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/standing-orders/publications/"],
    "Statutory Instruments Committee (Commons)": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/statutory-instruments-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/statutory-instruments-committee/publications/"],
    "Sub-Committee on Disinformation": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/digital-culture-media-and-sport-committee/sub-committee-on-disinformation/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/digital-culture-media-and-sport-committee/sub-committee-on-disinformation/publications/"],
    "Sub-Committee on the Work of the Independent Commission for Aid Impact": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/international-development-committee/sub-committee-on-the-work-of-the-independent-commission-for-aid-impact1/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/international-development-committee/sub-committee-on-the-work-of-the-independent-commission-for-aid-impact1/publications/"],
    "Transport Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/transport-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/transport-committee/publications/"],
    "Treasury Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/treasury-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/treasury-committee/publications/"],
    "Treasury Sub-Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/treasury-committee/treasury-sub-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/treasury-committee/treasury-sub-committee/publications/"],
    "Welsh Affairs Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/welsh-affairs-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/welsh-affairs-committee/publications/"],
    "Women and Equalities Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/women-and-equalities-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/women-and-equalities-committee/publications/"],
    "Work and Pensions Committee": ["https://www.parliament.uk/business/committees/committees-a-z/commons-select/work-and-pensions-committee/", "https://www.parliament.uk/business/committees/committees-a-z/commons-select/work-and-pensions-committee/publications/"]
}
