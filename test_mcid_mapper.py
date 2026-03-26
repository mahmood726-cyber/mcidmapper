"""
test_mcid_mapper.py — 20 Selenium tests for MCID Mapper
Tests: core math, classification logic, UI interactions, examples, export, dark mode, ARIA tabs
"""

import io
import json
import math
import os
import sys
import time
import unittest

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mcid-mapper.html')
FILE_URL = 'file:///' + HTML_PATH.replace('\\', '/')


def get_driver():
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--window-size=1280,900')
    opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(3)
    return driver


class TestMCIDMapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        cls.driver.get(FILE_URL)
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def js(self, script):
        return self.driver.execute_script(script)

    def reload(self):
        self.driver.get(FILE_URL)
        time.sleep(0.5)

    # === Test 1: Page loads and title present ===
    def test_01_page_loads(self):
        title = self.driver.title
        self.assertIn('MCID', title)
        h1 = self.driver.find_element(By.CSS_SELECTOR, '.app-header h1')
        self.assertIn('MCID', h1.text)

    # === Test 2: normalCDF correctness ===
    def test_02_normalCDF(self):
        # CDF(0) = 0.5
        val = self.js("return window.__MCID_MAPPER__.normalCDF(0)")
        self.assertAlmostEqual(val, 0.5, places=6)
        # CDF(1.96) ~ 0.975
        val2 = self.js("return window.__MCID_MAPPER__.normalCDF(1.96)")
        self.assertAlmostEqual(val2, 0.975, places=2)
        # CDF(-1.96) ~ 0.025
        val3 = self.js("return window.__MCID_MAPPER__.normalCDF(-1.96)")
        self.assertAlmostEqual(val3, 0.025, places=2)

    # === Test 3: normalQuantile correctness ===
    def test_03_normalQuantile(self):
        val = self.js("return window.__MCID_MAPPER__.normalQuantile(0.5)")
        self.assertAlmostEqual(val, 0.0, places=4)
        val2 = self.js("return window.__MCID_MAPPER__.normalQuantile(0.975)")
        self.assertAlmostEqual(val2, 1.96, places=1)

    # === Test 4: classify — exercise example is likely clinically significant ===
    # |CI_upper|=0.42 < MCID=0.5 so CI crosses threshold; point estimate beyond
    def test_04_classify_exercise(self):
        cls = self.js("return window.__MCID_MAPPER__.classify(-0.62, -0.81, -0.42, 0.5, 'negative')")
        self.assertEqual(cls, 'likely_significant')

    # === Test 5: classify — homeopathy is NOT clinically significant ===
    def test_05_classify_homeopathy(self):
        cls = self.js("return window.__MCID_MAPPER__.classify(-0.11, -0.20, -0.02, 0.5, 'negative')")
        self.assertEqual(cls, 'not_significant')

    # === Test 6: classify — statins for LDL is clinically significant ===
    def test_06_classify_statins(self):
        cls = self.js("return window.__MCID_MAPPER__.classify(-38, -42, -34, 25, 'negative')")
        self.assertEqual(cls, 'significant')

    # === Test 7: classify — uncertain case (CI crosses MCID, point below) ===
    def test_07_classify_uncertain(self):
        # effect = -0.3, CI = -0.6 to 0.0, MCID = 0.5, direction negative
        # |effect| = 0.3 < 0.5, but |CI lower| = 0.6 > 0.5
        cls = self.js("return window.__MCID_MAPPER__.classify(-0.3, -0.6, 0.0, 0.5, 'negative')")
        self.assertEqual(cls, 'uncertain')

    # === Test 8: classify — likely significant (point beyond, CI crosses) ===
    def test_08_classify_likely(self):
        # effect = -0.55, CI = -0.8 to -0.3, MCID = 0.5
        # |effect| = 0.55 > 0.5, but |CI upper| = 0.3 < 0.5
        cls = self.js("return window.__MCID_MAPPER__.classify(-0.55, -0.8, -0.3, 0.5, 'negative')")
        self.assertEqual(cls, 'likely_significant')

    # === Test 9: computeProbBeyondMCID — exercise example ===
    def test_09_prob_exercise(self):
        prob = self.js("return window.__MCID_MAPPER__.computeProbBeyondMCID(-0.62, -0.81, -0.42, 0.5, 'negative').prob")
        self.assertGreater(prob, 0.80)  # Should be high probability

    # === Test 10: computeProbBeyondMCID — homeopathy example ===
    def test_10_prob_homeopathy(self):
        prob = self.js("return window.__MCID_MAPPER__.computeProbBeyondMCID(-0.11, -0.20, -0.02, 0.5, 'negative').prob")
        self.assertLess(prob, 0.10)  # Should be very low

    # === Test 11: Example button loads data and runs analysis ===
    def test_11_example_button_exercise(self):
        self.reload()
        btn = self.driver.find_element(By.CSS_SELECTOR, '[data-example="exercise"]')
        btn.click()
        time.sleep(0.5)
        state = self.js("return window.__MCID_MAPPER__.getState()")
        self.assertAlmostEqual(state['effect'], -0.62, places=2)
        # CI crosses MCID but point estimate beyond => likely_significant
        self.assertEqual(state['classification'], 'likely_significant')

    # === Test 12: Example button — homeopathy ===
    def test_12_example_button_homeopathy(self):
        self.reload()
        btn = self.driver.find_element(By.CSS_SELECTOR, '[data-example="homeopathy"]')
        btn.click()
        time.sleep(0.5)
        state = self.js("return window.__MCID_MAPPER__.getState()")
        self.assertEqual(state['classification'], 'not_significant')

    # === Test 13: Tab switching via ARIA tabs ===
    def test_13_tab_switching(self):
        self.reload()
        viz_tab = self.driver.find_element(By.ID, 'tab-viz')
        viz_tab.click()
        time.sleep(0.3)
        panel = self.driver.find_element(By.ID, 'panel-viz')
        self.assertIn('active', panel.get_attribute('class'))
        self.assertEqual(viz_tab.get_attribute('aria-selected'), 'true')
        # Input tab should be inactive
        input_tab = self.driver.find_element(By.ID, 'tab-input')
        self.assertEqual(input_tab.get_attribute('aria-selected'), 'false')

    # === Test 14: Dark mode toggle ===
    def test_14_dark_mode(self):
        self.reload()
        body_classes = self.driver.find_element(By.TAG_NAME, 'body').get_attribute('class')
        was_dark = 'dark' in body_classes
        toggle = self.driver.find_element(By.ID, 'themeToggle')
        toggle.click()
        time.sleep(0.3)
        body_classes2 = self.driver.find_element(By.TAG_NAME, 'body').get_attribute('class')
        is_dark_now = 'dark' in body_classes2
        self.assertNotEqual(was_dark, is_dark_now)

    # === Test 15: MCID library renders all items ===
    def test_15_mcid_library(self):
        items = self.driver.find_elements(By.CSS_SELECTOR, '.mcid-library-item')
        self.assertEqual(len(items), 10)

    # === Test 16: MCID library click fills MCID input ===
    def test_16_library_click(self):
        self.reload()
        items = self.driver.find_elements(By.CSS_SELECTOR, '.mcid-library-item')
        # Click "SF-36 Physical" (index 2, MCID = 3)
        items[2].click()
        time.sleep(0.3)
        mcid_val = self.driver.find_element(By.ID, 'inputMCID').get_attribute('value')
        self.assertEqual(mcid_val, '3')
        etype = Select(self.driver.find_element(By.ID, 'inputEffectType'))
        self.assertEqual(etype.first_selected_option.get_attribute('value'), 'MD')

    # === Test 17: Clear button resets state ===
    def test_17_clear(self):
        # Load example first
        self.js("window.__MCID_MAPPER__.loadExample('exercise')")
        time.sleep(0.3)
        state = self.js("return window.__MCID_MAPPER__.getState()")
        self.assertIsNotNone(state['effect'])
        # Clear
        self.js("window.__MCID_MAPPER__.clearInputs()")
        time.sleep(0.3)
        state2 = self.js("return window.__MCID_MAPPER__.getState()")
        self.assertIsNone(state2['effect'])

    # === Test 18: escapeHtml works ===
    def test_18_escapeHtml(self):
        result = self.js("return window.__MCID_MAPPER__.escapeHtml('<script>alert(1)</script>')")
        self.assertNotIn('<script>', result)
        self.assertIn('&lt;', result)

    # === Test 19: csvSafe handles formula injection ===
    def test_19_csvSafe(self):
        result = self.js("return window.__MCID_MAPPER__.csvSafe('=CMD()')")
        self.assertTrue(result.startswith("'") or result.startswith('"'))
        # Should not start with = after safing
        # Normal values pass through
        normal = self.js("return window.__MCID_MAPPER__.csvSafe('hello')")
        self.assertEqual(normal, 'hello')

    # === Test 20: Ratio measure classification (RR below 1) ===
    def test_20_ratio_classification(self):
        # RR = 0.80, CI = 0.70 to 0.91, MCID = 0.95, direction ratio_below
        # |log(0.80)| = 0.223 > |log(0.95)| = 0.051, entire CI below 0.95
        cls = self.js("return window.__MCID_MAPPER__.classify(0.80, 0.70, 0.91, 0.95, 'ratio_below')")
        self.assertEqual(cls, 'significant')
        # RR = 0.98, CI = 0.92 to 1.04, MCID = 0.95
        # log(0.98) = -0.02, log(CI upper=1.04) = 0.039 > -|log(0.95)|=-0.051 => not significant
        cls2 = self.js("return window.__MCID_MAPPER__.classify(0.98, 0.92, 1.04, 0.95, 'ratio_below')")
        self.assertIn(cls2, ['not_significant', 'uncertain'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
