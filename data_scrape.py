# scraper.py
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def get_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Use system ChromeDriver in WSL
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_site(url, search_term, click_selectors=None, item_selector="li.product-list-item"):
    """
    url: website URL
    search_term: term to search
    click_selectors: list of CSS selectors to click before searching
    item_selector: CSS selector for the items to scrape
    """
    driver = get_driver(headless=True)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(url)
        print("🟢success", f"Page loaded: {driver.title}")

        # Click optional elements
        if click_selectors:
            for sel in click_selectors:
                try:
                    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
                    element.click()
                    print("🟢click", f"Clicked element: {sel}")
                    time.sleep(1)  # wait for page update
                except Exception as e:
                    print("🟡warning", f"Could not click {sel}: {e}")

        # Find search box dynamically
        search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea#autocomplete-search-bar")))
        print("🟢success", "Search bar found!")
        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        print("🟢search", f"Searching for '{search_term}'...")

        # Wait for results
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, item_selector)))
        items = driver.find_elements(By.CSS_SELECTOR, item_selector)
        print("🟢success", f"Found {len(items)} items")

        return items

    except Exception as e:
        print("error", f"Scraping failed: {e}")
        return []
    finally:
        driver.quit()
def scrape_products():
    driver = get_driver(headless=True)
    wait = WebDriverWait(driver, 20)
    
    try:
        items = scrape_site(
            url="https://www.bestbuy.com/",
            search_term="laptop",
            click_selectors=["a.us-link"],  
            item_selector="li.product-list-item"
        )
        # driver.get("https://www.bestbuy.com/")

        # print("🟢 Page title:", driver.title)


        # us_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.us-link")))
        # us_link.click()
        # print("Clicked United States link...")
        # wait.until(EC.title_contains("Official Online Store"))
        # print("🟢 Page title:", driver.title)


        # search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea#autocomplete-search-bar")))
        # print("🟢 Search bar found!")
        
        # search_box.clear()
        # search_box.send_keys("laptop")
        # search_box.send_keys(Keys.RETURN)
        # print("Searching for laptops...")
        # wait.until(EC.title_contains("laptop"))
        # print("🟢 Page title:", driver.title)
        # items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product-list-item")))
        # print(f"🟢 found {len(items)}items ")
        products = []
        for item in items:
            try:
                time.sleep(5)
                title = item.find_element(By.CSS_SELECTOR, "h2.product-title").text
                price = item.find_element(By.CSS_SELECTOR, "div[data-testid='price-block-customer-price'] span").text
                link = item.find_element(By.CSS_SELECTOR, "a.product-list-item-link").get_attribute("href")
                time.sleep(5)
                products.append({
                    "title": title,
                    "price": price,
                    "link": link
                })
                time.sleep(5)
            except Exception as e:
                print("⚠️ Skipped product:", e)
                continue

        print(f"🟢Found {len(products)} products")
        
        # ✅ Now visit each product link and get review data
        for product in products:
            try:
                print(f"🔍 Visiting: {product['title']} ...")
                driver.get(product["link"])

                # wait for review section or fallback to default
                try:
                    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#customer-reviews")))
                    customer_reviews_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='See All Customer Reviews']]")))
                    customer_reviews_btn.click()
                    print("Clicked Customer Reviews Button...")
                    # wait.until(EC.title_contains("Official Online Store"))
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.c-section-title.heading-5.v-fw-medium")))
                    # wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.font-sans.text-style-body-md-500")))
                    # reviews_container = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[8]/div[2]/div/ul[2]")))
                    # print("Found container with absolute XPath!")
                    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.list-unstyled.border-sm-none")))
                    review_items = reviews_container.find_elements(By.CSS_SELECTOR, "li.w-full.py-300.py-sm-200.border-light")
                    reviews_data = []
                    for review in review_items:
                        try:
                            rating = review.find_element(By.CSS_SELECTOR, "span.sr-only").text
                        except:
                            rating = "N/A"

                        try:
                            title = review.find_element(By.CSS_SELECTOR, "h4.body-copy-lg").text
                        except:
                            title = "N/A"

                        try:
                            content = review.find_element(By.CSS_SELECTOR, "p.body-copy-lg").text
                        except:
                            content = "N/A"

                        try:
                            posted_by = review.find_element(By.CSS_SELECTOR, "p[data-testid='posted-by']").text
                        except:
                            posted_by = "N/A"

                        reviews_data.append({
                            "rating": rating,
                            "title": title,
                            "content": content,
                            "posted_by": posted_by
                        })

                    print(f"✅ Extracted {len(reviews_data)} reviews.")
                    
                except:
                    print("⚠️ No review section found, skipping review extraction.")
                    product["rating"] = "N/A"
                    product["review_count"] = "N/A"
                    continue

            except Exception as e:
                print("⚠️ Failed to get reviews for:", product["title"], e)
                continue

        # ✅ Optional: print all product data with reviews
        print("\n📊 Final product list with reviews:")
        for p in products:
            print(p)

       
        
        
        # Save raw data
        with open("data/products_raw.json", "w", encoding="utf-8") as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(products)} products")
        return products
        
    finally:
        driver.quit()

