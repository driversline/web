import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def check_domain_availability(domain, max_retries=1):
    attempts = 0
    while attempts < max_retries:
        try:
            print(f"Checking domain: {domain}")
            try:
                response = requests.get(f"http://{domain}", timeout=1)
                if response.status_code == 200:
                    print(f"{domain} - Available via HTTP")
                    return domain, True
            except requests.RequestException:
                print(f"{domain} - HTTP unavailable")

            try:
                response = requests.get(f"https://{domain}", timeout=1)
                if response.status_code == 200:
                    print(f"{domain} - Available via HTTPS")
                    return domain, True
            except requests.RequestException:
                print(f"{domain} - HTTPS unavailable")

            return domain, False
        except Exception as e:
            attempts += 1
            print(f"Error checking {domain}. Retry {attempts} of {max_retries}... Error: {e}")
            time.sleep(1)
    return domain, False

def main():
    base_domain = "!"
    tlds = [
        ".com", ".net", ".org", ".info", ".biz", ".co", ".me", ".io", ".ai",
        ".ru", ".us", ".de", ".jp", ".uk", ".fr", ".au", ".ca", ".it", ".es",
        ".nl", ".se", ".ch", ".no", ".fi", ".dk", ".pl", ".cz", ".hk", ".in",
        ".br", ".mx", ".za", ".tv", ".cc", ".ws", ".xyz", ".online", ".site",
        ".tech", ".store", ".app", ".dev", ".cloud", ".space", ".fun", ".love",
        ".life", ".pro", ".name", ".mobi", ".tel", ".asia", ".jobs", ".coop",
        ".museum", ".int", ".aero", ".cat", ".travel", ".fm", ".am", ".bz",
        ".design", ".digital", ".media", ".photography", ".art", ".fashion",
        ".health", ".money", ".news", ".today", ".tips", ".world", ".zone",
        ".city", ".group", ".team", ".family", ".club", ".community", ".events",
        ".solutions", ".services", ".systems", ".technology", ".ventures",
        ".works", ".expert", ".consulting", ".agency", ".marketing", ".finance",
        ".financial", ".investments", ".properties", ".realestate", ".rent",
        ".property", ".house", ".homes", ".land", ".build", ".construction",
        ".contractors", ".builders", ".renovations", ".remodeling", ".repairs",
        ".cleaning", ".plumbing", ".electric", ".landscaping", ".pestcontrol",
        ".moving", ".storage", ".transportation", ".logistics", ".shipping",
        ".courier", ".delivery", ".food", ".restaurant", ".cafe", ".bar",
        ".pub", ".catering", ".cooking", ".kitchen", ".chef", ".baking",
        ".bakery", ".recipe", ".dining", ".meal", ".snack", ".drink",
        ".beverage", ".cocktail", ".wine", ".beer", ".spirits", ".liquor",
        ".distillery", ".brewery", ".winery", ".tasting", ".event", ".festival",
        ".party", ".celebration", ".wedding", ".anniversary", ".birthday",
        ".holiday", ".vacation", ".travel", ".tourism", ".adventure",
        ".exploration", ".expedition", ".journey", ".trip", 
        ".academy", ".accountant", ".actor", ".agency", ".app", ".art", ".associates",
        ".attorney", ".auction", ".audio", ".band", ".bar", ".bargains", ".beer",
        ".best", ".bid", ".bike", ".bio", ".black", ".blog", ".blue", ".boutique",
        ".builders", ".business", ".buzz", ".cab", ".camera", ".camp", ".capital",
        ".cards", ".care", ".careers", ".cash", ".catering", ".center", ".chat",
        ".cheap", ".church", ".city", ".claims", ".cleaning", ".clothing", ".club",
        ".coffee", ".community", ".company", ".computer", ".consulting", ".contractors",
        ".cool", ".country", ".coupons", ".dance", ".dating", ".deals", ".design",
        ".diamonds", ".digital", ".directory", ".discount", ".doctor", ".dog",
        ".domains", ".education", ".email", ".energy", ".engineer", ".engineering",
        ".events", ".exchange", ".expert", ".family", ".fashion", ".finance",
        ".financial", ".fitness", ".flights", ".florist", ".flowers", ".food",
        ".fund", ".furniture", ".gallery", ".games", ".garden", ".gifts", ".glass",
        ".global", ".gold", ".golf", ".graphics", ".green", ".guitars", ".guru",
        ".health", ".holiday", ".house", ".immo", ".in", ".info", ".institute",
        ".insurance", ".international", ".investments", ".jewelry", ".jobs",
        ".kitchen", ".land", ".law", ".lawyer", ".lease", ".life", ".lighting",
        ".limited", ".live", ".loans", ".love", ".ltd", ".management", ".market",
        ".marketing", ".media", ".meet", ".mobi", ".money", ".mortgage", ".movie",
        ".music", ".name", ".news", ".online", ".party", ".photography", ".photos",
        ".pics", ".place", ".plumbing", ".pro", ".productions", ".properties",
        ".property", ".pub", ".recipes", ".rent", ".repair", ".report", ".reviews",
        ".rocks", ".run", ".sale", ".school", ".services", ".shop", ".site",
        ".solutions", ".space", ".store", ".style", ".sucks", ".systems", ".tech",
        ".technology", ".tips", ".today", ".tools", ".trade", ".training", ".travel",
        ".tv", ".university", ".ventures", ".video", ".villas", ".vision", ".vote",
        ".watch", ".web", ".website", ".works", ".world", ".zone",
        ".abogado", ".ac", ".ad", ".ae", ".aero", ".af", ".ag", ".ai", ".al",
        ".am", ".ao", ".aq", ".ar", ".as", ".at", ".au", ".aw", ".ax", ".az",
        ".ba", ".bb", ".bd", ".be", ".bf", ".bg", ".bh", ".bi", ".bj", ".bm",
        ".bn", ".bo", ".br", ".bs", ".bt", ".bv", ".bw", ".by", ".bz", ".ca",
        ".cc", ".cd", ".cf", ".cg", ".ch", ".ci", ".ck", ".cl", ".cm", ".cn",
        ".co", ".cr", ".cu", ".cv", ".cw", ".cx", ".cy", ".cz", ".de", ".dj",
        ".dk", ".dm", ".do", ".dz", ".ec", ".edu", ".ee", ".eg", ".es", ".et",
        ".eu", ".fi", ".fj", ".fm", ".fo", ".fr", ".ga", ".gb", ".gd", ".ge",
        ".gf", ".gg", ".gh", ".gi", ".gl", ".gm", ".gn", ".gp", ".gq", ".gr",
        ".gt", ".gu", ".gw", ".gy", ".hk", ".hm", ".hn", ".hr", ".ht", ".hu",
        ".id", ".ie", ".il", ".im", ".in", ".io", ".iq", ".ir", ".is", ".it",
        ".je", ".jm", ".jo", ".jp", ".ke", ".kg", ".kh", ".ki", ".kj", ".km",
        ".kn", ".kp", ".kr", ".kw", ".ky", ".kz", ".la", ".lb", ".lc", ".li",
        ".lk", ".lr", ".ls", ".lt", ".lu", ".lv", ".ly", ".ma", ".mc", ".md",
        ".me", ".mg", ".mh", ".mk", ".ml", ".mm", ".mn", ".mo", ".mp", ".mq",
        ".mr", ".ms", ".mt", ".mu", ".mv", ".mw", ".mx", ".my", ".mz", ".na",
        ".nc", ".ne", ".nf", ".ng", ".ni", ".nl", ".no", ".np", ".nr", ".nu",
        ".nz", ".om", ".org", ".pa", ".pe", ".pf", ".pg", ".ph", ".pk", ".pl",
        ".pm", ".pn", ".pr", ".pt", ".pw", ".py", ".qa", ".re", ".ro", ".rs", 
        ".ru", ".rw", ".sa", ".sb", ".sc", ".sd", ".se", ".sg", ".sh",
        ".si", ".sj", ".sk", ".sl", ".sm", ".sn", ".so", ".sr", ".ss", ".st",
        ".su", ".sv", ".sx", ".sy", ".sz", ".tc", ".td", ".tf", ".tg", ".th",
        ".tj", ".tk", ".tl", ".tm", ".tn", ".to", ".tr", ".ts", ".tt", ".tv",
        ".tz", ".ua", ".ug", ".uk", ".us", ".uy", ".uz", ".va", ".vc", ".ve",
        ".vg", ".vi", ".vn", ".vu", ".wf", ".ye", ".yt", ".za", ".zm", ".zw"
    ]
    
    domains = [base_domain + tld for tld in tlds]
    working_domains = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_domain = {executor.submit(check_domain_availability, domain): domain for domain in domains}
        
        for future in as_completed(future_to_domain):
            domain, is_working = future.result()
            if is_working:
                working_domains.append(domain)

    print("Working domains:")
    if working_domains:
        for domain in working_domains:
            print(domain)
    else:
        print("No working domains.")

if __name__ == "__main__":
    main()
       

