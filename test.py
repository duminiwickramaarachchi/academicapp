from playwright.sync_api import sync_playwright
import os
import time

# =========================
# CONFIG
# =========================

BASE_URL = "https://academicapp-1.onrender.com"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

LECTURER_USERNAME = "Gihan"
LECTURER_PASSWORD = "123456"

STUDENT_USERNAME = "Nipun"
STUDENT_PASSWORD = "123456"

# =========================
# SCREENSHOT FOLDER
# =========================

os.makedirs("screenshots", exist_ok=True)


def snap(page, name):
    page.screenshot(path=f"screenshots/{name}.png")


# =========================
# LOGIN FUNCTION
# =========================

def login(page, username, password, screenshot_name):

    page.goto(BASE_URL, wait_until="networkidle")

    page.fill("input[name='username']", username)
    page.fill("input[name='password']", password)

    snap(page, screenshot_name)

    page.click("button[type='submit']")

    page.wait_for_load_state("networkidle")

    time.sleep(2)


# =========================
# MAIN TEST
# =========================

def run():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
        )

        # ====================================================
        # 1. ADMIN LOGIN
        # ====================================================

        admin = browser.new_page()

        login(
            admin,
            ADMIN_USERNAME,
            ADMIN_PASSWORD,
            "01_admin_login"
        )

        snap(admin, "02_admin_dashboard")

        print("ADMIN LOGIN SUCCESS")

        # ====================================================
        # 2. CREATE USER
        # ====================================================

        try:

            admin.goto(f"{BASE_URL}/admin")

            admin.fill(
                "input[name='username']",
                "teststudent"
            )

            admin.fill(
                "input[name='password']",
                "123456"
            )

            admin.select_option(
                "select[name='role']",
                "student"
            )

            snap(admin, "03_create_user_form")

            admin.locator(
                "button:has-text('Create User')"
            ).click()

            admin.wait_for_load_state("networkidle")

            snap(admin, "04_user_created")

            print("CREATE USER SUCCESS")

        except Exception as e:
            print("CREATE USER FAILED")
            print(e)

        # ====================================================
        # 3. CREATE SUBJECT
        # ====================================================

        try:

            admin.goto(f"{BASE_URL}/admin")

            admin.fill(
                "input[name='name']",
                "Test Subject"
            )

            admin.fill(
                "form[action='/create_subject'] input[name='lecturer_id']",
                "3"
            )

            snap(admin, "05_create_subject_form")

            admin.locator(
                "form[action='/create_subject'] button"
            ).click()

            admin.wait_for_load_state("networkidle")

            snap(admin, "06_subject_created")

            print("CREATE SUBJECT SUCCESS")

        except Exception as e:
            print("CREATE SUBJECT FAILED")
            print(e)

        # ====================================================
        # 4. ENROLL STUDENT
        # ====================================================

        try:

            admin.goto(f"{BASE_URL}/admin")

            enroll_form = admin.locator(
                "form[action='/enroll_student']"
            )

            enroll_form.locator(
                "input[name='student_id']"
            ).fill("5")

            enroll_form.locator(
                "input[name='subject_id']"
            ).fill("1")

            snap(admin, "07_enroll_student_form")

            enroll_form.locator(
                "button"
            ).click()

            admin.wait_for_load_state("networkidle")

            snap(admin, "08_student_enrolled")

            print("ENROLL STUDENT SUCCESS")

        except Exception as e:
            print("ENROLL STUDENT FAILED")
            print(e)

        # ====================================================
        # 5. CHANGE LECTURER
        # ====================================================

        try:

            admin.goto(f"{BASE_URL}/admin")

            change_form = admin.locator(
                "form[action='/change_lecturer']"
            )

            change_form.locator(
                "input[name='subject_id']"
            ).fill("1")

            change_form.locator(
                "input[name='lecturer_id']"
            ).fill("7")

            snap(admin, "09_change_lecturer_form")

            change_form.locator(
                "button"
            ).click()

            admin.wait_for_load_state("networkidle")

            snap(admin, "10_lecturer_changed")

            print("CHANGE LECTURER SUCCESS")

        except Exception as e:
            print("CHANGE LECTURER FAILED")
            print(e)

        # ====================================================
        # 6. LOGOUT ADMIN
        # ====================================================

        try:

            admin.goto(f"{BASE_URL}/logout")

            admin.wait_for_load_state("networkidle")

            snap(admin, "11_admin_logout")

            print("ADMIN LOGOUT SUCCESS")

        except Exception as e:
            print("ADMIN LOGOUT FAILED")
            print(e)

        # ====================================================
        # 7. LECTURER LOGIN
        # ====================================================

        lecturer = browser.new_page()

        login(
            lecturer,
            LECTURER_USERNAME,
            LECTURER_PASSWORD,
            "12_lecturer_login"
        )

        lecturer.goto(
            f"{BASE_URL}/lecturer_dashboard"
        )

        lecturer.wait_for_load_state("networkidle")

        snap(lecturer, "13_lecturer_dashboard")

        print("LECTURER LOGIN SUCCESS")

        # ====================================================
        # 8. SAVE MARKS
        # ====================================================

        try:

            marks_inputs = lecturer.locator(
                "input[name='marks']"
            )

            marks_inputs.first.fill("85")

            snap(lecturer, "14_marks_form")

            lecturer.locator(
                "button:has-text('Save')"
            ).first.click()

            lecturer.wait_for_load_state("networkidle")

            snap(lecturer, "15_marks_saved")

            print("SAVE MARKS SUCCESS")

        except Exception as e:
            print("SAVE MARKS FAILED")
            print(e)

        # ====================================================
        # 9. LOGOUT LECTURER
        # ====================================================

        try:

            lecturer.goto(f"{BASE_URL}/logout")

            lecturer.wait_for_load_state("networkidle")

            snap(lecturer, "16_lecturer_logout")

            print("LECTURER LOGOUT SUCCESS")

        except Exception as e:
            print("LECTURER LOGOUT FAILED")
            print(e)

        # ====================================================
        # 10. STUDENT LOGIN
        # ====================================================

        student = browser.new_page()

        login(
            student,
            STUDENT_USERNAME,
            STUDENT_PASSWORD,
            "17_student_login"
        )

        student.goto(
            f"{BASE_URL}/student_dashboard"
        )

        student.wait_for_load_state("networkidle")

        snap(student, "18_student_dashboard")

        print("STUDENT LOGIN SUCCESS")

        # ====================================================
        # 11. STUDENT LOGOUT
        # ====================================================

        try:

            student.goto(f"{BASE_URL}/logout")

            student.wait_for_load_state("networkidle")

            snap(student, "19_student_logout")

            print("STUDENT LOGOUT SUCCESS")

        except Exception as e:
            print("STUDENT LOGOUT FAILED")
            print(e)

        # ====================================================
        # END
        # ====================================================

        browser.close()

        print("\nALL TESTS COMPLETED SUCCESSFULLY")


run()