# backend/hybrid_search.py
from playwright.sync_api import sync_playwright
from deepface import DeepFace
import cv2
import requests
import numpy as np
import os
import uuid

def download_image(url):
    try:
        response = requests.get(url, timeout=10)
        img_array = np.frombuffer(response.content, np.uint8)
        return cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    except:
        return None

def run_yandex_search(image_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://yandex.com/images/")
        page.click("text=Search by image")
        page.set_input_files("input[type='file']", image_path)
        page.wait_for_timeout(7000)

        links = page.query_selector_all("a.serp-item__link")
        image_urls = [link.get_attribute("href") for link in links[:10]]
        browser.close()
        return image_urls

def find_similar_faces(uploaded_img_path):
    yandex_urls = run_yandex_search(uploaded_img_path)
    results = []

    for url in yandex_urls:
        img = download_image(url)
        if img is None:
            continue

        try:
            result = DeepFace.verify(img1_path=uploaded_img_path, img2_path=img, enforce_detection=False)
            if result["verified"]:
                results.append({
                    "url": url,
                    "score": result["distance"]
                })
        except:
            continue

    return results
