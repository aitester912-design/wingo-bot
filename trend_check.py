from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import time


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Yeh line webdriver-manager ka use karke error khatam kar degi
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    driver.switch_to.default_content()
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if iframes: driver.switch_to.frame(iframes[0])

    print("=" * 50)
    print("BOT STARTED")
    print("=" * 50)

    total_pages_to_scan = 50
    flat_game_chain = []

    for page in range(1, total_pages_to_scan + 1):
        WebDriverWait(driver, 10).until(
            lambda d: len(d.find_elements(By.XPATH, "//*[normalize-space()='B' or normalize-space()='S']")) > 0
        )
        elements = driver.find_elements(By.XPATH, "//*[normalize-space()='B' or normalize-space()='S']")

        page_results = []
        for el in elements:
            txt = el.text.strip().upper()
            if txt == "B": page_results.append("BIG")
            elif txt == "S": page_results.append("SMALL")

        if page_results:
            # Yahan enumerate add kiya hai taake round index mile
            for i, item in enumerate(page_results):
                flat_game_chain.append({"result": item, "page": page, "round_idx": i + 1})
            print(f"Page {page} scanned | Results found: {len(page_results)}")
        else:
            print(f"Page {page} : No data found")

        if page == total_pages_to_scan: break

        clicked = False
        anchor_element = None
        try:
            anchor_element = driver.find_element(By.XPATH, f"//*[contains(text(), '{page}/50') or contains(text(), '{page} / 50')]")
            ActionChains(driver).move_to_element(anchor_element).move_by_offset(60, 0).click().perform()
            clicked = True
            print(f"Next page click success")
        except:
            try:
                if anchor_element:
                    parent = anchor_element.find_element(By.XPATH, "..")
                    last_btn = parent.find_element(By.XPATH, "./*[last()]")
                    driver.execute_script("arguments[0].click();", last_btn)
                    clicked = True
                    print("Fallback click success")
            except: pass
        
        if not clicked:
            print(f"Page {page} par next click fail."); break
        time.sleep(2)

    # --- Streak Calculation & Location Tracking ---
    max_big, max_small = 0, 0
    big_range = {"start_p": 0, "end_p": 0, "start_r": 0, "end_r": 0}
    small_range = {"start_p": 0, "end_p": 0, "start_r": 0, "end_r": 0}
    
    curr_big, curr_small = 0, 0
    t_big = {"p": 0, "r": 0}
    t_small = {"p": 0, "r": 0}

    for item in flat_game_chain:
        res, p, r = item["result"], item["page"], item["round_idx"]
        if res == "BIG":
            if curr_big == 0: t_big = {"p": p, "r": r}
            curr_big += 1; curr_small = 0
            if curr_big > max_big:
                max_big = curr_big
                big_range = {"start_p": t_big["p"], "end_p": p, "start_r": t_big["r"], "end_r": r}
        else:
            if curr_small == 0: t_small = {"p": p, "r": r}
            curr_small += 1; curr_big = 0
            if curr_small > max_small:
                max_small = curr_small
                small_range = {"start_p": t_small["p"], "end_p": p, "start_r": t_small["r"], "end_r": r}

    # FINAL REPORT
    total_big = sum(1 for x in flat_game_chain if x["result"] == "BIG")
    total_small = sum(1 for x in flat_game_chain if x["result"] == "SMALL")

    print("\n" + "=" * 50 + "\nFINAL REPORT\n" + "=" * 50)
    print(f"Total Rounds : {len(flat_game_chain)}")
    print(f"BIG Count    : {total_big}")
    print(f"SMALL Count  : {total_small}")

    print(f"\nLongest BIG Streak: {max_big}")
    print(f"  Start: Page {big_range['start_p']}, Round {big_range['start_r']}")
    print(f"  End:   Page {big_range['end_p']}, Round {big_range['end_r']}")
    
    print(f"\nLongest SMALL Streak: {max_small}")
    print(f"  Start: Page {small_range['start_p']}, Round {small_range['start_r']}")
    print(f"  End:   Page {small_range['end_p']}, Round {small_range['end_r']}")

# ... (yahan aapka report print ho raha hai)
    print(f"  End:   Page {small_range['end_p']}, Round {small_range['end_r']}")

    # Line 112 ke paas yahan add karein:


except Exception as e:
    print("ERROR:", e)
