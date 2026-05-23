from playwright.sync_api import sync_playwright
print("Playwright installed successfully")

import os
from playwright.sync_api import sync_playwright

import time

BASE_URL = "https://academicapp-1.onrender.com"

# Create folder for screenshots
os.makedirs("screenshots", exist_ok=True)


def snap(page, name):
    page.screenshot(path=f"screenshots/{name}.png")


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # ----------------------------
        # 1. HOME / LOGIN PAGE
        # ----------------------------
        page.goto(BASE_URL)
        snap(page, "01_login_page")

        page.fill("input[name='username']", "admin")
        page.fill("input[name='password']", "admin123")
        snap(page, "02_login_filled")

        page.click("button[type='submit']")
        page.wait_for_timeout(2000)

        snap(page, "03_after_login_redirect")

        print("LOGIN DONE")

        # ----------------------------
        # 2. ADMIN DASHBOARD
        # ----------------------------
        page.goto(f"{BASE_URL}/admin")
        snap(page, "04_admin_dashboard")

        # ----------------------------
        # 3. CREATE USER
        # ----------------------------
        try:
            page.fill("input[name='username']", "testuser2")
            page.fill("input[name='password']", "1234")
            page.select_option("select[name='role']", "student")

            snap(page, "05_create_user_form")

            page.click("button[type='submit']")
            page.wait_for_timeout(1000)

            snap(page, "06_user_created")
            print("CREATE USER OK")

        except:
            print("CREATE USER FAILED")

        # ----------------------------
        # 4. CREATE SUBJECT
        # ----------------------------
        try:
            page.fill("input[name='name']", "Drawing")
            page.fill("input[name='lecturer_id']", "1")

            snap(page, "07_create_subject_form")

            page.click("button[type='submit']")
            page.wait_for_timeout(1000)

            snap(page, "08_subject_created")
            print("CREATE SUBJECT OK")

        except:
            print("CREATE SUBJECT FAILED")

        # ----------------------------
        # 5. ENROLL STUDENT
        # ----------------------------
        try:
            page.fill("input[name='student_id']", "2")
            page.fill("input[name='subject_id']", "1")

            snap(page, "09_enroll_form")

            page.click("button[type='submit']")
            page.wait_for_timeout(1000)

            snap(page, "10_student_enrolled")
            print("ENROLL OK")

        except:
            print("ENROLL FAILED")

        # ----------------------------
        # 6. LECTURER DASHBOARD
        # ----------------------------
        page.goto(BASE_URL)
        page.fill("input[name='username']", "Gihan")
        page.fill("input[name='password']", "123456")
        page.click("button[type='submit']")

        page.wait_for_timeout(2000)

        page.goto(f"{BASE_URL}/lecturer_dashboard")
        snap(page, "11_lecturer_dashboard")

        # ----------------------------
        # 7. SAVE MARKS
        # ----------------------------
        try:
            page.fill("input[name='student_id']", "2")
            page.fill("input[name='subject_id']", "1")
            page.fill("input[name='marks']", "85")

            snap(page, "12_marks_form")

            page.click("button[type='submit']")
            page.wait_for_timeout(1000)

            snap(page, "13_marks_saved")
            print("MARKS SAVED")

        except:
            print("MARKS FAILED")

        # ----------------------------
        # 8. STUDENT DASHBOARD
        # ----------------------------
        page.goto(BASE_URL)
        page.fill("input[name='username']", "Nipun")
        page.fill("input[name='password']", "123456")
        page.click("button[type='submit']")

        page.wait_for_timeout(2000)

        page.goto(f"{BASE_URL}/student_dashboard")
        snap(page, "14_student_dashboard")

        # ----------------------------
        # 9. LOGOUT
        # ----------------------------
        page.goto(f"{BASE_URL}/logout")
        snap(page, "15_logout")

        print("ALL TESTS COMPLETED")

        browser.close()


run()