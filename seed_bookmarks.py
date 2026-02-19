from app import app, db, Category, Link

# Final Screenshot Data with exact Dynamic parameters for FTO and 100 Days
seed_data = [
    {
        "name": "APPLICATIONS", "is_application": True, "sort_order": 1,
        "links": [
            {"title": "PDF", "icon": "mdi mdi-file-pdf-box", "url": "https://pdf.palojori.in/", "is_dynamic": False},
            {"title": "WHATSAPP", "icon": "mdi mdi-whatsapp", "url": "https://web.whatsapp.com/", "is_dynamic": False},
            {"title": "TOOLS", "icon": "mdi mdi-tools", "url": "https://tools.palojori.in/", "is_dynamic": False},
            {"title": "DOWNLOADS", "icon": "mdi mdi-download", "url": "https://download.palojori.in/", "is_dynamic": False},
            {"title": "NREGA BOT", "icon": "mdi mdi-robot", "url": "https://nregabot.com/", "is_dynamic": False},
            {"title": "FILES", "icon": "mdi mdi-folder", "url": "https://files.palojori.in/", "is_dynamic": False},
            {"title": "NREGA CULPRIT", "icon": "mdi mdi-account-alert", "url": "https://reports.palojori.in/", "is_dynamic": False},
        ]
    },
    {
        "name": "BLOCK", "is_application": False, "sort_order": 2,
        "links": [
            {"title": "PO LOGIN", "icon": "mdi mdi-shield-account", "url": "https://nregade4.nic.in/netnrega/Login.aspx?&level=HomePO&state_code=34", "is_dynamic": False},
            {"title": "New Tab", "icon": "mdi mdi-open-in-new", "url": "https://nregade4.nic.in/Netnrega/progofficer/Poindexframe2.aspx", "is_dynamic": False},
            {"title": "Fasal Bima", "icon": "mdi mdi-sprout", "url": "https://fasal.palojori.in/", "is_dynamic": False},
            {"title": "Admin Login", "icon": "mdi mdi-account-key", "url": "https://nregade4.nic.in/netnrega/login.aspx?&level=HomePODBA&state_code=34", "is_dynamic": False},
            {"title": "Delete Allocation", "icon": "mdi mdi-delete-outline", "url": "https://nregade4.nic.in/Netnrega/delWrkAlloc.aspx", "is_dynamic": False},
            {"title": "Delete Demand", "icon": "mdi mdi-delete-outline", "url": "https://nregade4.nic.in/Netnrega/deletedemand.aspx", "is_dynamic": False},
            {"title": "PNB", "icon": "mdi mdi-bank", "url": "https://mgnrega.jharkhand.gov.in/admin/Account/Login/?ReturnUrl=%2Fadmin", "is_dynamic": False},
            {"title": "Jal doot", "icon": "mdi mdi-water", "url": "https://mnregaweb4.nic.in/JaldootWeb/Login.aspx", "is_dynamic": False},
            {"title": "AYASAD", "icon": "mdi mdi-leaf", "url": "https://sarkaraapkedwar.jharkhand.gov.in/#/login", "is_dynamic": False},
            {"title": "Yuktdhara", "icon": "mdi mdi-map", "url": "https://bhuvan-cas1.nrsc.gov.in/cas/login?service=https%3A%2F%2Fbhuvan-app2.nrsc.gov.in%2Fplanner_v3%2Findex.php", "is_dynamic": False},
            {"title": "Secure", "icon": "mdi mdi-lock", "url": "https://secure.nic.in/secure/jharkhand", "is_dynamic": False},
            {"title": "Bhuvan Nrega", "icon": "mdi mdi-earth", "url": "https://bhuvan-app2.nrsc.gov.in/mgnrega/mgnrega_phase2.php", "is_dynamic": False},
        ]
    },
    {
        "name": "PANCHAYAT", "is_application": False, "sort_order": 3,
        "links": [
            {"title": "Panchayat DATA Entry", "icon": "mdi mdi-keyboard", "url": "https://nregade4.nic.in/Netnrega/Login.aspx?&level=HomeGP&state_code=34", "is_dynamic": False},
            {"title": "Demand Formate", "icon": "mdi mdi-file-document", "url": "https://tools.palojori.in/demand/", "is_dynamic": False},
            {"title": "PS Login", "icon": "mdi mdi-login", "url": "https://mnregaweb3.nic.in/Netnrega/FTO/Login.aspx?&level=HomeACGP&state_code=34", "is_dynamic": False},
            {"title": "Mukhiya Login", "icon": "mdi mdi-login", "url": "https://mnregaweb3.nic.in/Netnrega/FTO/Login.aspx?&level=HomeWLGP&state_code=34", "is_dynamic": False},
            {"title": "BPO Login", "icon": "mdi mdi-login", "url": "https://mnregaweb3.nic.in/Netnrega/FTO/Login.aspx?&level=HomeAC&state_code=34", "is_dynamic": False},
            {"title": "BDO Login", "icon": "mdi mdi-login", "url": "https://mnregaweb3.nic.in/Netnrega/FTO/Login.aspx?&level=HomeWL&state_code=34", "is_dynamic": False},
            {"title": "JE Login", "icon": "mdi mdi-login", "url": "https://nregade4.nic.in/netnrega/Login.aspx?&level=HomeGPMB&state_code=34", "is_dynamic": False},
            {"title": "AE Login", "icon": "mdi mdi-login", "url": "https://nregade4.nic.in/netnrega/Login.aspx?&level=HomePOMB&state_code=34", "is_dynamic": False},
            {"title": "Workcode", "icon": "mdi mdi-code-tags", "url": "https://workcode.palojori.in/", "is_dynamic": False},
            {"title": "Download MR Pdf", "icon": "mdi mdi-file-pdf", "url": "https://mr.palojori.in/", "is_dynamic": False},
        ]
    },
    {
        "name": "MUSTER ROLL", "is_application": False, "sort_order": 4,
        "links": [
            {"title": "Demand", "icon": "mdi mdi-hand-coin", "url": "https://nregade4.nic.in/Netnrega/demand_new.aspx", "is_dynamic": False},
            {"title": "Allocation", "icon": "mdi mdi-sitemap", "url": "https://nregade4.nic.in/Netnrega/workalloc.aspx", "is_dynamic": False},
            {"title": "Generate MR", "icon": "mdi mdi-file-plus", "url": "https://nregade4.nic.in/Netnrega/preprintmsr.aspx", "is_dynamic": False},
            {"title": "Fill MR", "icon": "mdi mdi-pencil", "url": "https://nregade4.nic.in/Netnrega/fillprintedmsr.aspx", "is_dynamic": False},
            {"title": "Edit MR", "icon": "mdi mdi-file-edit", "url": "https://nregade4.nic.in/Netnrega/mustrollattend_edit.aspx", "is_dynamic": False},
            {"title": "MR Payment", "icon": "mdi mdi-cash", "url": "https://nregade4.nic.in/Netnrega/msrpayment.aspx", "is_dynamic": False},
            {"title": "Wagelist", "icon": "mdi mdi-format-list-bulleted", "url": "https://nregade4.nic.in/Netnrega/SendMSRtoPO.aspx", "is_dynamic": False},
            {"title": "Remove Non-DBT", "icon": "mdi mdi-account-remove", "url": "https://nregade4.nic.in/Netnrega/delmsr.aspx", "is_dynamic": False},
            {"title": "Send Wagelist", "icon": "mdi mdi-send", "url": "https://nregade4.nic.in/Netnrega/sendforpay.aspx", "is_dynamic": False},
            {"title": "Re-Print MR", "icon": "mdi mdi-printer", "url": "https://nregade4.nic.in/Netnrega/reprintmsr.aspx", "is_dynamic": False},
            {"title": "Zero MR", "icon": "mdi mdi-numeric-0-box", "url": "https://nregade4.nic.in/Netnrega/musteraszero.aspx", "is_dynamic": False},
        ]
    },
    {
        "name": "REPORTS", "is_application": False, "sort_order": 5,
        "links": [
            {"title": "MIS", "icon": "mdi mdi-chart-bar", "url": "https://nreganarep.nic.in/netnrega/MISreport4.aspx", "is_dynamic": False},
            {"title": "Reports", "icon": "mdi mdi-file-chart", "url": "https://nregastrep.nic.in/netnrega/homestciti.aspx?state_code=34&state_name=JHARKHAND&lflag=eng&labels=labels", "is_dynamic": False},
            
            {"title": "District Report", "icon": "mdi mdi-city", "url": "https://nregastrep.nic.in/netnrega/Homedist.aspx?flag_debited=&is_statefund=&lflag=eng&district_code=[DIST_CODE]&district_name=[DIST_NAME]&state_name=[STATE_NAME]&state_Code=[STATE_CODE]", "is_dynamic": True},
            {"title": "Panchayat Report", "icon": "mdi mdi-home-group", "url": "https://nregastrep.nic.in/netnrega/Progofficer/PoIndexFrame.aspx?flag_debited=S&lflag=eng&District_Code=[DIST_CODE]&district_name=[DIST_NAME]&state_name=[STATE_NAME]&state_Code=[STATE_CODE]&finyear=[FIN_YEAR]&check=1&block_name=[BLOCK_NAME]&Block_Code=[BLOCK_CODE]", "is_dynamic": True},
            
            {"title": "Dashboard", "icon": "mdi mdi-view-dashboard", "url": "https://mnregaweb4.nic.in/netnrega/no_of_mrs_report.aspx?page=S&lflag=eng&state_name=JHARKHAND&state_code=34&fin_year=2025-2026&source=national&Digest=/iH40rNMc6riDA1zg5kR0g", "is_dynamic": False},
            {"title": "Issued MR", "icon": "mdi mdi-file-check", "url": "https://nreganarep.nic.in/netnrega/dpc_sms_new.aspx?lflag=eng&page=s&short_name=JH&state_name=JHARKHAND&state_code=34&fin_year=2025-2026&source=national&Digest=OXdGUcDxGNP1328mWk5gxQ", "is_dynamic": False},
            {"title": "Dynamic Report", "icon": "mdi mdi-chart-dynamic", "url": "https://nreganarep.nic.in/netnrega/dynamic_work_details.aspx?page=S&lflag=eng&state_name=JHARKHAND&state_code=34&fin_year=2025-2026&source=national&Digest=/iH40rNMc6riDA1zg5kR0g", "is_dynamic": False},
            
            # FTO aur 100 Days ko poori tarah dynamic kar diya gaya hai (bina Digest ke)
            {"title": "FTO", "icon": "mdi mdi-bank-transfer", "url": "https://nregastrep.nic.in/netnrega/FTO/FTOReport.aspx?page=b&mode=B&lflag=eng&flg=W&state_name=[STATE_NAME]&state_code=[STATE_CODE]&district_name=[DIST_NAME]&district_code=[DIST_CODE]&block_code=[BLOCK_CODE]&block_name=[BLOCK_NAME]&fin_year=[FIN_YEAR]&dstyp=P", "is_dynamic": True},
            {"title": "100 Days", "icon": "mdi mdi-calendar-check", "url": "https://nregastrep.nic.in/netnrega/state_html/empspecifydays.aspx?lflag=eng&district_code=[DIST_CODE]&district_name=[DIST_NAME]&state_code=[STATE_CODE]&state_name=[STATE_NAME]&page=B&fin_year=[FIN_YEAR]", "is_dynamic": True},
            
            {"title": "Search", "icon": "mdi mdi-magnify", "url": "https://mnregaweb4.nic.in/netnrega/homesearch.htm", "is_dynamic": False},
            {"title": "DPR", "icon": "mdi mdi-file-document-outline", "url": "https://mnregaweb4.nic.in/netnrega/state_html/wrk_cat_freeze.aspx?page=S&short_name=JH&state_name=JHARKHAND&state_code=34&fin_year=2025-2026&source=national&Digest=p+7GuzGC80H4v81L/5sWog", "is_dynamic": False},
            {"title": "PMAY", "icon": "mdi mdi-home", "url": "https://pmayg.gov.in/netiayHome/home.aspx", "is_dynamic": False},
            {"title": "MR Tracking", "icon": "mdi mdi-radar", "url": "https://nregastrep.nic.in/netnrega/dynamic_muster_track.aspx?lflag=eng&state_code=34&fin_year=2025-2026&state_name=JHARKHAND&Digest=FjAL4jfLQiHS1NU1KnbRZg", "is_dynamic": False},
        ]
    },
    {
        "name": "LABOUR", "is_application": False, "sort_order": 6,
        "links": [
            {"title": "Check Labour Card", "icon": "mdi mdi-account-search", "url": "https://nregade4.nic.in/Netnrega/UID/UidStatus.aspx", "is_dynamic": False},
            {"title": "New Jobcard", "icon": "mdi mdi-card-account-details-outline", "url": "https://nregade4.nic.in/Netnrega/EntryReg.aspx?LinkBPL=N", "is_dynamic": False},
            {"title": "Add UID", "icon": "mdi mdi-fingerprint", "url": "https://nregade4.nic.in/Netnrega/BulkAadhaarUpdate.aspx", "is_dynamic": False},
            {"title": "Add A/C", "icon": "mdi mdi-bank-plus", "url": "https://nregade4.nic.in/Netnrega/EditAppBank.aspx", "is_dynamic": False},
            {"title": "Freeze AC", "icon": "mdi mdi-snowflake", "url": "https://nregade4.nic.in/Netnrega/states/Freez_ac.aspx", "is_dynamic": False},
            {"title": "Jobcard Verification", "icon": "mdi mdi-check-decagram", "url": "https://nregade4.nic.in/Netnrega/VerificationJCatPO.aspx", "is_dynamic": False},
            {"title": "Issue", "icon": "mdi mdi-file-export", "url": "https://nregade4.nic.in/Netnrega/Issues_JC.aspx", "is_dynamic": False},
            {"title": "Resume", "icon": "mdi mdi-play-circle-outline", "url": "https://nregade4.nic.in/Netnrega/ResumeApp.aspx", "is_dynamic": False},
            {"title": "ABPS", "icon": "mdi mdi-account-cash", "url": "https://nregade4.nic.in/Netnrega/UID/VUID_NPCI.aspx", "is_dynamic": False},
        ]
    },
    {
        "name": "SEMI-SKILLED", "is_application": False, "sort_order": 7,
        "links": [
            {"title": "Register Mate&Mistri", "icon": "mdi mdi-account-hard-hat", "url": "https://nregade4.nic.in/Netnrega/Registration_sk.aspx", "is_dynamic": False},
            {"title": "Freeze SSK", "icon": "mdi mdi-snowflake-alert", "url": "https://nregade4.nic.in/Netnrega/states/Freeze_SSKac.aspx", "is_dynamic": False},
            {"title": "Fill SSK MR", "icon": "mdi mdi-clipboard-edit", "url": "https://nregade4.nic.in/Netnrega/mateworker_dtl.aspx", "is_dynamic": False},
            {"title": "Generate SSK wagelist", "icon": "mdi mdi-clipboard-list", "url": "https://nregade4.nic.in/Netnrega/skillwagelist.aspx", "is_dynamic": False},
            {"title": "Send SSK wagelist", "icon": "mdi mdi-send-check", "url": "https://nregade4.nic.in/Netnrega/skillwagelistsend.aspx", "is_dynamic": False},
        ]
    },
    {
        "name": "MATERIAL", "is_application": False, "sort_order": 8,
        "links": [
            {"title": "Voucher Entry", "icon": "mdi mdi-receipt", "url": "https://nregade4.nic.in/Netnrega/billdetail.aspx", "is_dynamic": False},
            {"title": "Plantation Voucher", "icon": "mdi mdi-tree", "url": "https://nregade4.nic.in/Netnrega/billdetail_reg.aspx", "is_dynamic": False},
            {"title": "Material List", "icon": "mdi mdi-view-list", "url": "https://nregade4.nic.in/Netnrega/Gen_Voucher.aspx", "is_dynamic": False},
        ]
    },
    {
        "name": "WORKS", "is_application": False, "sort_order": 9,
        "links": [
            {"title": "New Work", "icon": "mdi mdi-shovel", "url": "https://nregade4.nic.in/Netnrega/serverphotoupload.aspx?count=661", "is_dynamic": False},
            {"title": "Edit Work (IF)", "icon": "mdi mdi-pencil-ruler", "url": "https://nregade4.nic.in/Netnrega/IFEdit.aspx", "is_dynamic": False},
            {"title": "Update Estimate", "icon": "mdi mdi-calculator", "url": "https://nregade4.nic.in/Netnrega/Update_proposedstatus.aspx", "is_dynamic": False},
            {"title": "Freeze DPR", "icon": "mdi mdi-file-lock", "url": "https://nregade4.nic.in/Netnrega/states/DPCApprove_Work.aspx", "is_dynamic": False},
            {"title": "Close Scheme", "icon": "mdi mdi-door-closed", "url": "https://nregade4.nic.in/Netnrega/compwork.aspx", "is_dynamic": False},
            {"title": "Delete Work", "icon": "mdi mdi-delete-forever", "url": "https://nregade4.nic.in/Netnrega/DeleteWork.aspx", "is_dynamic": False},
        ]
    }
]

def seed_database():
    with app.app_context():
        # Pehle purane links clean kar lo (taaki duplicate na ho)
        Link.query.delete()
        Category.query.delete()
        db.session.commit()
        
        print("🌱 Seeding Categories and Links with Original URLs...")
        for cat_data in seed_data:
            cat = Category(name=cat_data["name"], is_application=cat_data["is_application"], sort_order=cat_data["sort_order"])
            db.session.add(cat)
            db.session.commit()
            
            for link_data in cat_data["links"]:
                link = Link(title=link_data["title"], icon_class=link_data["icon"], url=link_data["url"], is_dynamic=link_data["is_dynamic"], category_id=cat.id)
                db.session.add(link)
            db.session.commit()
            print(f"✅ Added Category: {cat.name} with {len(cat_data['links'])} links.")
        print("🎉 Migration Complete! Check your dashboard.")

if __name__ == '__main__':
    seed_database()