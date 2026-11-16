# Wordlist Clinic & Target Profiling — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Offensive_Tooling-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-brightgreen.svg)
![Topic](https://img.shields.io/badge/Topic-Wordlist_Generation-orange.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete penetration testing writeup and methodology guide for the **Wordlists** room on TryHackMe, demonstrating targeted dictionary scraping with CeWL, username permutation modeling, and credential spraying against `tryfinanceme.local`.

---

## 📋 Executive Summary
Standard wordlists like `rockyou.txt` frequently fail against enterprise targets enforcing custom password policies. This room demonstrates building highly tailored, target-specific wordlists: scraping website vocabulary with `cewl`, sanitizing word pools, generating realistic username combinations from employee registries, and executing targeted password spraying.

* **Target Domain:** `tryfinanceme.local`
* **Artifacts in Directory:**
  * `cewl_words.txt` / `words_clean.txt` / `words_raw.txt`: Scraped & sanitized web dictionaries
  * `names.txt`: Target employee roster
  * `users_first.last.txt` / `users_flast.txt` / `users_firstl.txt`: Username permutations
  * `pass_helios.txt`: Tailored candidate password list

---

## 🔍 Stage 1: Web Scraping with CeWL

### 1.1 Spidering the Target
Using `cewl` to extract unique words of minimum length 6 from `tryfinanceme.local`:
```bash
cewl -d 2 -m 6 http://tryfinanceme.local -w cewl_words.txt
```

### 1.2 Wordlist Cleaning & Normalization
Sanitizing the raw words (`words_raw.txt`) by stripping punctuation, converting to lowercase, and sorting unique entries into `words_clean.txt`:
```bash
tr '[:upper:]' '[:lower:]' < words_raw.txt | tr -d '[:punct:]' | sort -u > words_clean.txt
```

---

## 👥 Stage 2: Username Permutation Modeling

Given target employee names in `names.txt` (e.g. *Alex Johnson*, *Kevin Zhang*, *Rachel Williams*), corporate systems typically follow predictable username schemas:

1. **First Name . Last Name (`users_first.last.txt`):**
   `alex.johnson`, `kevin.zhang`, `rachel.williams`
2. **First Initial + Last Name (`users_flast.txt`):**
   `ajohnson`, `kzhang`, `rwilliams`
3. **First Name + Last Initial (`users_firstl.txt`):**
   `alexj`, `kevinz`, `rachelw`

These lists are generated via shell/Python scripts to match enterprise Active Directory conventions.

---

## 🎯 Stage 3: Password Spraying & Optimization

Using the generated username lists and custom password candidates (`pass_helios.txt`), we execute low-frequency password spraying via Kerbrute or Hydra to avoid account lockout thresholds:
```bash
hydra -L users_flast.txt -P pass_helios.txt tryfinanceme.local smb
```

---

## 🛡️ Remediation
1. **Password Complexity & Ban Lists:** Implement domain password filters (such as Azure AD Password Protection) that reject passwords containing corporate names, seasonal terms, or scraped website keywords.
2. **Account Lockout Policies:** Enforce progressive lockouts to mitigate automated credential spraying attacks.
