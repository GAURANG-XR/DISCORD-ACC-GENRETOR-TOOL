import os
import threading
import colorama
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import string

def banner():
    author = "arnox-dev"
    ultimate = """ █    ██  ██▓  ▄▄▄█████▓ ██▓ ███▄ ▄███▓ ▄▄▄     ▄▄▄█████▓▓█████      
 ██  ▓██▒▓██▒  ▓  ██▒ ▓▒▓██▒▓██▒▀█▀ ██▒▒████▄   ▓  ██▒ ▓▒▓█   ▀      
▓██  ▒██░▒██░  ▒ ▓██░ ▒░▒██▒▓██    ▓██░▒██  ▀█▄ ▒ ▓██░ ▒░▒███        
▓▓█  ░██░▒██░  ░ ▓██▓ ░ ░██░▒██    ▒██ ░██▄▄▄▄██░ ▓██▓ ░ ▒▓█  ▄      
▒▒█████▓ ░██████▒▒██▒ ░ ░██░▒██▒   ░██▒ ▓█   ▓██▒ ▒██▒ ░ ░▒████▒     
░▒▓▒ ▒ ▒ ░ ▒░▓  ░▒ ░░   ░▓  ░ ▒░   ░  ░ ▒▒   ▓▒█░ ▒ ░░   ░░ ▒░ ░     
░░▒░ ░ ░ ░ ░ ▒  ░  ░     ▒ ░░  ░      ░  ▒   ▒▒ ░   ░     ░ ░  ░     
 ░░░ ░ ░   ░ ░   ░       ▒ ░░      ░     ░   ▒    ░         ░        
   ░         ░  ░        ░         ░         ░  ░           ░  ░     """   
    made_by = f"[ Made By {author} ]"
    try:
        console_width = os.get_terminal_size().columns
    except OSError:
        console_width = 80 # Fallback for environments without terminal size
        
    ultimate_lines = ultimate.splitlines()
    centered_ultimate = "\n".join(line.center(console_width) for line in ultimate_lines)
    centered_made_by = made_by.center(console_width)
    print(f"{Fore.RED}{Style.BRIGHT}{centered_ultimate}\n{centered_made_by}")

from datetime import datetime

class ultimate:
    def __init__(self, input_file) -> None:
        colorama.init()
        self.input_file = input_file
        self.lock = threading.Lock()
        # Stylized prefixes
        self.p_info = f"{Fore.CYAN}[{datetime.now().strftime('%H:%M:%S')}] {Fore.BLUE}[INFO]{Fore.RESET}"
        self.p_success = f"{Fore.CYAN}[{datetime.now().strftime('%H:%M:%S')}] {Fore.GREEN}[SUCCESS]{Fore.RESET}"
        self.p_error = f"{Fore.CYAN}[{datetime.now().strftime('%H:%M:%S')}] {Fore.RED}[ERROR]{Fore.RESET}"
        self.p_warn = f"{Fore.CYAN}[{datetime.now().strftime('%H:%M:%S')}] {Fore.YELLOW}[WARN]{Fore.RESET}"
        self.p_action = f"{Fore.CYAN}[{datetime.now().strftime('%H:%M:%S')}] {Fore.MAGENTA}[ACTION]{Fore.RESET}"
        
        self.accounts = self.load_accounts()

    def load_accounts(self):
        accounts = []
        if not os.path.exists(self.input_file):
            return accounts
        with open(self.input_file, 'r', encoding='utf8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if ':' not in line:
                    continue
                accounts.append(line)
        return accounts
    
    def log(self, message, level="info"):
        prefix = self.p_info
        if level == "success": prefix = self.p_success
        elif level == "error": prefix = self.p_error
        elif level == "warn": prefix = self.p_warn
        elif level == "action": prefix = self.p_action
        
        with self.lock:
             # Refresh timestamp
            timestamp = f"{Fore.CYAN}[{datetime.now().strftime('%H:%M:%S')}]"
            # Reconstruct prefix with new time if needed, or just use generic
            print(f"{prefix.split('] ')[0].split(' ')[0]} {prefix.split('] ')[1]} {message}")

    def print(self, arg): # Keep for backward compatibility if needed, but redirect to log
        with self.lock:
            print(arg)

    def remove_account(self, email):
        if not self.accounts: return
        self.accounts = [acc for acc in self.accounts if not acc.startswith(email)]
        with open(self.input_file, 'w', encoding='utf8') as f:
            f.write('\n'.join(self.accounts))

    def save_account(self, email, password):
        os.makedirs("./data", exist_ok=True)
        with open("./data/accounts.txt", "a", encoding='utf8') as f:
            f.write(f'{email}:{password}\n')
        self.log(f"Account credentials saved for {email}", "success")

    def save_token(self, email, password, token):
        os.makedirs("./data", exist_ok=True)
        with open("./data/tokens.txt", "a") as f:
            f.write(f'{email}:{password}:{token}\n')
        self.log(f"Token saved to data/tokens.txt", "success")

    def generate_random_credentials(self):
        # Generate random email and password
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        email = f"user_{random_str}@gmail.com" 
        
        password_chars = string.ascii_letters + string.digits + "!@#$%"
        password = ''.join(random.choices(password_chars, k=12))
        return email, password

    def __gen__(self, email: str, password: str, headless: bool = True) -> None:
        driver = None
        try:
            mode_str = "Headless" if headless else "Visible"
            self.log(f"Initializing browser for {Fore.CYAN}{email}{Fore.RESET} ({mode_str} Mode)...", "action")
            
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
                options.page_load_strategy = 'eager' # Fast for headless
            else:
                options.page_load_strategy = 'normal' # Stable for visible
            
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            

            driver_path = ChromeDriverManager().install()
            if "THIRD_PARTY_NOTICES" in driver_path:
                base_dir = os.path.dirname(driver_path)
                driver_path = os.path.join(base_dir, "chromedriver")
            
            if not os.access(driver_path, os.X_OK):
                os.chmod(driver_path, 0o755)

            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            
            self.log("Navigating to Discord registration...", "info")
            driver.get('https://discord.com/register')
            
            wait = WebDriverWait(driver, 20) # Increased initial wait
            
            self.log("Entering account credentials...", "action")
            wait.until(EC.element_to_be_clickable((By.NAME, 'email'))).send_keys(email)
            
            # Display Name (global_name)
            try:
                driver.find_element(By.NAME, 'global_name').send_keys(email.split('@')[0])
            except:
                pass # Optional or might not be present in all regions/versions?
            
            driver.find_element(By.NAME, 'username').send_keys(email.split('@')[0])
            driver.find_element(By.NAME, 'password').send_keys(password)
            
            self.log("Setting Date of Birth...", "action")
            # Improved DOB handling with explicit waits/clicks if needed
            pw_field = driver.find_element(By.NAME, 'password')
            pw_field.send_keys(Keys.TAB)
            time.sleep(0.5) # Wait for focus move
            
            actions = webdriver.ActionChains(driver)
            actions.send_keys("May")
            actions.send_keys(Keys.ENTER).perform()
            
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys("15")
            actions.send_keys(Keys.ENTER).perform()
            
            actions.send_keys(Keys.TAB).perform()
            actions.send_keys("1995")
            actions.send_keys(Keys.ENTER).perform() # Ensure year is also submitted/closed

            self.log("Submitting form...", "action")
            try:
                btns = driver.find_elements(By.TAG_NAME, "button")
                click_success = False
                for btn in btns:
                    if btn.text.lower() == "continue":
                        btn.click()
                        click_success = True
                        break
                if not click_success:
                     wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))).click()
            except:
                 pass

            # Fast Rate Limit Check
            try:
                if driver.find_elements(By.XPATH, "//*[contains(text(), 'The resource is being rate limited')]"):
                     self.log("Rate Limit detected! Skipping account.", "error")
                     driver.quit()
                     return
            except:
                pass

            self.log("Checking for Captcha...", "info")
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='hcaptcha']")))
                frames = driver.find_elements(By.CSS_SELECTOR, "iframe[src*='hcaptcha']")
                for frame in frames:
                    try:
                        driver.switch_to.frame(frame)
                        checkbox = driver.find_elements(By.ID, "checkbox")
                        if checkbox:
                            checkbox[0].click()
                            self.log("Auto-clicked 'I am human' checkbox.", "success")
                        driver.switch_to.default_content()
                    except:
                        driver.switch_to.default_content()
            except:
                self.log("No visible Captcha iframe found immediately.", "info")

            self.log(f"Waiting for account creation success ({mode_str})...", "info")
            timeout = 30 if headless else 600
            
            try:
                WebDriverWait(driver, timeout).until(EC.url_contains("discord.com/channels/@me"))
                self.log(f"Account created successfully!", "success")
                
                self.save_account(email, password)
                self.remove_account(email)
                
                self.log("Extracting token...", "action")
                time.sleep(2) 
                token = None
                for _ in range(3):
                    token = driver.execute_script(r"try{return window.localStorage.getItem('token')}catch(e){return null}")
                    if token: break
                    time.sleep(1)

                if token:
                    token = token.replace('"', '').strip()
                    self.save_token(email, password, token)
                else:
                     self.log("Token not in storage. Attempting fallback login...", "warn")
                     driver.quit()
                     self.login_and_fetch_token(email, password)
            except:
                 if headless:
                     self.log(f"Headless failed/timed out. Falling back to VISIBLE mode for {email}...", "warn")
                     driver.quit()
                     time.sleep(2) # Give OS time to reclaim resources
                     self.__gen__(email, password, headless=False)
                     return
                 else:
                     self.log(f"Registration timed out even in visible mode.", "error")

        except Exception as e:
            if headless:
                 self.log(f"Headless Check failed ({str(e)[:100]}...). Retrying VISIBLE...", "warn")
                 if driver: 
                     try: driver.quit() 
                     except: pass
                 time.sleep(2)
                 self.__gen__(email, password, headless=False)
            else:
                self.log(f"Critical error in Visible Mode: {str(e)}", "error")
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass

    def login_and_fetch_token(self, email: str, password: str) -> None:
        driver = None
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.page_load_strategy = 'eager'

            driver_path = ChromeDriverManager().install()
            if "THIRD_PARTY_NOTICES" in driver_path:
                base_dir = os.path.dirname(driver_path)
                driver_path = os.path.join(base_dir, "chromedriver")
            
            if not os.access(driver_path, os.X_OK):
                os.chmod(driver_path, 0o755)

            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            
            # Fast login
            driver.get('https://discord.com/login')
            wait = WebDriverWait(driver, 10)
            
            wait.until(EC.element_to_be_clickable((By.NAME, 'email'))).send_keys(email)
            driver.find_element(By.NAME, 'password').send_keys(password)
            driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            
            try:
                WebDriverWait(driver, 15).until(EC.url_contains("discord.com/channels/@me"))
                time.sleep(2)
                token = driver.execute_script(r"try{return window.localStorage.getItem('token')}catch{return null}")
                
                if token:
                    token = token.replace('"', '').strip()  
                    self.save_token(email, password, token)
                else:
                    self.print(f'{self.lerror}{Fore.RED} Failed to retrieve token.')
            except:
                 self.print(f'{self.lerror}{Fore.RED} Login timed out.')
            
            driver.quit()
        except Exception as e:
            self.print(f'{self.lerror}{Fore.RED} Error during login: {str(e)}')
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    def __main__(self):
        if not self.accounts:
            self.log(f"No accounts found. Switching to Auto-Generation Mode.", "warn")
            how_many = 3
            self.log(f"Generating {how_many} random accounts...", "info")
            
            for i in range(how_many):
                email, password = self.generate_random_credentials()
                self.log(f"Processing Account {i+1}/{how_many}: {Fore.YELLOW}{email}{Fore.RESET}", "info")
                self.__gen__(email, password)
            return

        for account in self.accounts:
            parts = account.split(':', 1)
            if len(parts) != 2:
                self.log(f"Skipping invalid account entry: {account}", "warn")
                continue
            email, password = parts
            self.__gen__(email, password)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    input_file = './data/input.txt'
    ultimate(input_file).__main__()
