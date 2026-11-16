# The Letter — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-OSINT-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange.svg)
![Type](https://img.shields.io/badge/Type-Historical_Investigation-purple.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete investigative writeup for the **Letter** OSINT challenge on TryHackMe, analyzing water-damaged historical documents, regional French press archives (Gallica), and postal barcode tracking.

---

## 📋 Executive Summary
The Letter is an advanced historical OSINT room involving three primary artifacts: a water-damaged envelope bearing a French postal barcode (`letter.png`), a torn clipping from Brittany's regional newspaper *L'Ouest-Éclair* (`Newspaper_clipping.png`), and a handwritten letter from **Audette** addressed to **Édouard** (`Note.txt`). By decoding French postal routing markings and researching historical maritime rescue archives from May 1925 in Finistère via the French National Library (BnF Gallica), we identified the rescue hero and delivery postal code.

* **Category:** OSINT / Historical Document Analysis
* **Artifacts in Directory:**
  * `Note.txt`: Handwritten letter transcription
  * `letter.png`: Water-damaged envelope with postal barcode
  * `Newspaper_clipping.png`: Historical clipping from *L'Ouest-Éclair*
  * `L'Ouest-Éclair__bpt6k4965688.JPEG`: Full archived Gallica edition

---

## 🔍 Stage 1: Document & Clue Analysis

### 1.1 The Handwritten Letter (`Note.txt`)
The note provides essential narrative context:
> *"Mon cher Édouard, Aujourd'hui, en rangeant le grenier chez mes grands-parents, je suis tombée sur cette vieille coupure de journal. Ton arrière-grand-père n'avait même pas l'âge de passer le permis quand il s'est distingué ce jour-là. Le benjamin de l'équipe, et certainement pas le moins courageux..."*

**Key Intelligence Points:**
* **Sender:** Audette
* **Recipient:** Édouard (connected to SNSM / sea rescue services in Brittany)
* **Historical Event:** Édouard's great-grandfather was the youngest crew member (*le benjamin*) during a heroic maritime sea rescue when under legal driving age (<18 years old).

### 1.2 The Newspaper Clipping (`Newspaper_clipping.png`)
The clipping comes from the historical French regional paper *L'Ouest-Éclair* (Rennes / Finistère edition). Visible headlines mention political figures of the era (Painlevé, Herriot) and arctic explorer Roald Amundsen, dating the publication to **May 1925**.

---

## 📜 Stage 2: Archival Research (BnF Gallica)

Searching the digital archives of **Gallica** (Bibliothèque nationale de France) for *L'Ouest-Éclair* in May 1925:
* Matching edition identifier: `bpt6k4965688` (Dated May 1925).
* Inspecting regional news for the coastal department of **Finistère** (specifically Penmarc'h / Saint-Guénolé maritime rescue stations).
* In the aftermath of a severe storm hitting fishing vessels, a rescue crew launched a lifeboat. The article explicitly highlights the youngest crew member by name and age.

---

## 📬 Stage 3: Resolving Challenge Questions

### Question 1: Delivery Address Postal Code
* Decoding the orange postal routing barcode on `letter.png` and correlating with the Brittany SNSM rescue station location identifies the French postal code:
  * **Postal Code:** `29760` (Penmarc'h, Finistère)

### Question 2: Hero's Identity & Age (Flag)
* Cross-referencing the historical article text for the great-grandfather (*le benjamin*):
  * **Flag Format:** `THM{Name_Surname_age}`
  * Extracted hero details: First name, Surname, and reported age at the time of the 1925 disaster.

---

## 🛡️ Key Takeaways & OSINT Methodology
1. **Archive Exploration:** National historical newspaper repositories (like BnF Gallica or Chronicling America) are invaluable resources for verifying dates and contextual headlines.
2. **Postal Marking Analysis:** Standardized postal marks (barcodes, data matrices, postmarks) can confirm precise geographic jurisdictions even when physical written text is damaged.
