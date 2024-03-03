from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up the Selenium driver
chrome_options = Options()
chrome_options.add_argument("window-size=1200x600") 
chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
chrome_options.add_argument('--no-sandbox')  # Bypass OS security model, REQUIRED on Linux if running as root
chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

# Initialize the driver with the options
driver = webdriver.Chrome(options=chrome_options)

# Open the target URL
driver.get('https://www.ratemyprofessors.com/search/professors/825?q=*')

# Handle pop-ups (cookie consent, ads, etc.)
# Note: You need to replace 'XPATH_OF_POPUP_BUTTON' with the actual XPath of the popup close button.
try:
    # Try to click the close button using the container class
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/button'))
    ).click()
    print("Ad popup closed.")
except Exception as e:
    print("Ad popup could not be found or not clickable.")

counter=0; 
# Loop to click on the "Show More" button until it's no longer present
while True:
    try:
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".Buttons__Button-sc-19xdot-1.PaginationButton__StyledPaginationButton-txi1dr-1.eUNaBX"))
        )
        show_more_button.click()
        print("Clicked 'Show More' button.")
        counter =+ 1
        print(counter)

        # Wait for the new content to load
    except TimeoutException:
        # If the "Show More" button is not present, exit the loop
        print("No more 'Show More' buttons to click.")
        break

# Now, we'll extract the information for each professor card
professor_cards = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[class^='TeacherCard__InfoRatingWrapper']"))

)
professor_data = []

# Iterate through each professor card and extract information
for card in professor_cards:
    # Scroll into view of the card
    driver.execute_script("arguments[0].scrollIntoView(true);", card)
    
    # Extract the professor's name, department, and rating
    professor_name = card.find_element(By.CSS_SELECTOR, "[class^='CardName__StyledCardName']").text
    department = card.find_element(By.CSS_SELECTOR, "[class^='CardSchool__Department']").text
    rating = card.find_element(By.CSS_SELECTOR, "[class^='CardNumRating__CardNumRatingNumber']").text

    feedback_elements = card.find_elements(By.CSS_SELECTOR, "[class^='CardFeedback__CardFeedbackNumber']")
    # Extract "Would Take Again" and "Level of Difficulty" from feedback elements
    would_take_again = feedback_elements[0].text if len(feedback_elements) > 0 else "N/A"
    difficulty_lvl = feedback_elements[1].text if len(feedback_elements) > 1 else "N/A"
    prof_dict = {
        "Name": professor_name,
        "Department": department,
        "Rating": rating,
        "Would Take Again": would_take_again,
        "Difficulty Level": difficulty_lvl
    }
    professor_data.append(prof_dict)

    print(f"Professor Name: {professor_name}, Department: {department}, Rating: {rating}, Would Take Again: {would_take_again}, Difficulty Level: {difficulty_lvl}")

df = pd.DataFrame(professor_data)

# Specify the CSV file name
csv_file_name = 'professors.csv'

# Export the DataFrame to a CSV file
df.to_csv(csv_file_name, index=False)

print(f"Data exported to {csv_file_name} successfully.")

# Close the driver when done
driver.quit()

