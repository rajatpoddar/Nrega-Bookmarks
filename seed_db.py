import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from app import app, db, District, Block

# Jharkhand ke saare 24 Districts aur unke Codes
jharkhand_districts = [
    {"name": "BOKARO", "code": "3420"}, {"name": "CHATRA", "code": "3417"},
    {"name": "DEOGHAR", "code": "3422"}, {"name": "DHANBAD", "code": "3421"},
    {"name": "DUMKA", "code": "3411"}, {"name": "EAST SINGHBUM", "code": "3410"},
    {"name": "GARHWA", "code": "3407"}, {"name": "GIRIDIH", "code": "3419"},
    {"name": "GODDA", "code": "3415"}, {"name": "GUMLA", "code": "3403"},
    {"name": "HAZARIBAGH", "code": "3416"}, {"name": "JAMTARA", "code": "3412"},
    {"name": "KHUNTI", "code": "3424"}, {"name": "KODERMA", "code": "3418"},
    {"name": "LATEHAR", "code": "3406"}, {"name": "LOHARDAGA", "code": "3402"},
    {"name": "PAKUR", "code": "3414"}, {"name": "PALAMU", "code": "3405"},
    {"name": "RAMGARH", "code": "3423"}, {"name": "RANCHI", "code": "3401"},
    {"name": "SAHEBGANJ", "code": "3413"}, {"name": "SARAIKELA KHARSAWAN", "code": "3409"},
    {"name": "SIMDEGA", "code": "3404"}, {"name": "WEST SINGHBHUM", "code": "3408"}
]

def scrape_and_seed():
    with app.app_context():
        # --- FIX START: Skip scraping if data already exists ---
        if District.query.count() >= 24:
            print("✅ Districts and Blocks already exist in the database. Skipping scraping!")
            return
        # --- FIX END ---

        print("🚀 NREGA Web Scraper Started...")
        
        for dist_data in jharkhand_districts:
            # Check karo ki District pehle se DB me hai ya nahi
            district = District.query.filter_by(nrega_code=dist_data["code"]).first()
            if not district:
                district = District(name=dist_data["name"], nrega_code=dist_data["code"])
                db.session.add(district)
                db.session.commit()
            
            print(f"\n👉 Scraping Blocks for District: {district.name} ({district.nrega_code})")
            
            # NREGA District page URL
            url = f"https://nregastrep.nic.in/netnrega/Homedist.aspx?lflag=eng&district_code={district.nrega_code}&district_name={urllib.parse.quote(district.name)}&state_name=JHARKHAND&state_Code=34"
            
            try:
                # SSL verification hata diya kyunki NIC ki sites pe kabhi kabhi SSL error aata hai
                response = requests.get(url, verify=False, timeout=15)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # NREGA links se Block Code aur Name extract karne ke liye Regex
                added_blocks = set() # Duplicate blocks ignore karne ke liye
                
                for a_tag in soup.find_all('a', href=True):
                    href = a_tag['href']
                    if 'block_code=' in href.lower() and 'block_name=' in href.lower():
                        code_match = re.search(r'[bB]lock_[cC]ode=(\d+)', href)
                        name_match = re.search(r'block_name=([^&]+)', href)
                        
                        if code_match and name_match:
                            b_code = code_match.group(1)
                            # URL encoding theek karke safai se naam nikalna
                            b_name = urllib.parse.unquote(name_match.group(1)).replace('+', ' ').strip().upper()
                            
                            # Database me save karne ki logic
                            if b_code not in added_blocks:
                                existing_block = Block.query.filter_by(nrega_code=b_code).first()
                                if not existing_block:
                                    new_block = Block(name=b_name, nrega_code=b_code, district_id=district.id)
                                    db.session.add(new_block)
                                    print(f"   ✅ Added Block: {b_name} ({b_code})")
                                added_blocks.add(b_code)
                                
                db.session.commit()
            
            except Exception as e:
                print(f"   ❌ Error scraping {district.name}: {e}")

        print("\n🎉 Scraping and Database Seeding Complete!")

if __name__ == '__main__':
    # SSL Warning chhupane ke liye
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    scrape_and_seed()