# Missing Person — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-OSINT-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy/Medium-yellow.svg)
![Type](https://img.shields.io/badge/Type-Geolocation_&_EXIF-purple.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete investigative writeup for the **Missing Person** OSINT room on TryHackMe, focusing on image geolocation, EXIF metadata extraction, and social footprint analysis.

---

## 📋 Executive Summary
The scenario tasks investigators with tracing a missing traveler who vanished while attending a holiday trip centered around a 2025 MotoGP event. By inspecting two images (`motoGP.jpg` and `food.jpg`), we conducted reverse image search to geolocate the circuit in Indonesia, extracted exact camera timestamps via EXIF metadata, identified a local Mexican restaurant, and tracked down the missing individual's contact through social profiles.

* **Category:** OSINT / Geolocation
* **Artifacts in Directory:**
  * `osint-1767765507985.zip`: Provided challenge archive
  * `MotoGP.jpg`: Race track image
  * `food.jpg`: Restaurant dining image

---

## 🔍 Stage-by-Stage Investigation

### 🏁 Task 1: Identifying the Racing Circuit (`MotoGP.jpg`)
* **Objective:** Identify the commercial name of the circuit where the photo was taken.
* **Technique:** Google Reverse Image Search / Google Lens on `MotoGP.jpg` highlights the distinctive runoff patterns and grandstands.
* **Result:** **Pertamina Mandalika International Street Circuit** (Lombok, Indonesia).

### 📅 Task 2: Event Dates
* **Objective:** Determine when the MotoGP event took place at this circuit in 2025.
* **Technique:** Reviewing the official 2025 FIM MotoGP calendar for the Indonesian GP at Mandalika.
* **Answer:** `03-05/10/2025`

### 🌮 Task 3: Identifying the Restaurant (`food.jpg`)
* **Objective:** Find the name of the Mexican restaurant visited by the traveler.
* **Technique:** Inspecting `food.jpg` shows branded dining elements, menu designs, and tableware. Reverse searching the images and matching restaurants in Kuta Lombok / Mandalika reveals:
* **Answer:** **Cantina Mexicana**

### ⏰ Task 4: Timestamp Analysis (EXIF Data)
* **Objective:** Determine the exact time the photo was captured.
* **Technique:** Extracting embedded EXIF metadata using `exiftool`:
  ```bash
  exiftool food.jpg | grep -i "Date/Time Original"
  ```
* **Output:**
  ```text
  Date/Time Original              : 2025:10:04 19:55:30
  ```
* **Answer:** `19:55:30`

---

## 🌐 Stage 2: Event Tracing & Social Footprint

Following clues from the victim's journal:
* **After-Party:** The traveler met a local resident DJ at an event after-party in Lombok.
* **Social Discovery:** Searching Instagram/Facebook geo-tags for the venue on the night of October 4-5 uncovered the DJ's profile.
* **Local Guide Venture:** The DJ runs guided cave excursions. Reviewing business listings associated with his profile revealed the specific cave excursion location and contact telephone number required to conclude the investigation.

---

## 🛡️ Key Takeaways
1. **Metadata Hygiene:** Mobile devices automatically embed high-precision timestamps and GPS coordinates in JPEG EXIF tags unless explicitly scrubbed.
2. **Visual Correlation:** Minor background branding on table settings or napkins can be combined with known geographic boundaries to pinpoint exact establishments.
