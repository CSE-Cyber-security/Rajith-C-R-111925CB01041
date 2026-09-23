# Week 01 – Cybersecurity Asset Inventory System

A command-line Python application that helps a security administrator track
an organization's IT assets — workstations, servers, routers, switches, and
applications — along with each asset's risk level and security status.

## Problem Statement

Organizations manage many IT assets manually, which makes it hard to track
security status and know which assets need urgent attention. This system
lets an administrator **add, search, update, delete, and display** asset
records, and classifies each asset by **type**, **risk level**, and
**security status**.

## Features

- **Add Asset** – enter a new asset; every field is validated before it's saved
- **Display All Assets** – prints the full inventory plus summary counts
- **Search Asset** – look up one asset by Asset ID
- **Update Asset** – edit any field of an existing asset (leave a prompt blank to keep the current value)
- **Delete Asset** – remove an asset, with a confirmation step
- **Security Summary** – breakdown by risk level and security status, and a list of assets that need immediate attention (Critical risk or Vulnerable status)
- **Input validation** – Asset Type, Risk Level, and Security Status must match an allowed list; IP addresses must be valid dotted IPv4; required text fields can't be left empty
- **Persistence** – all changes are saved to `data/assets.json`, so the inventory survives between runs

## Data Fields

| Field | Notes |
|---|---|
| Asset ID | unique identifier |
| Asset Name | free text |
| Asset Type | Workstation / Server / Router / Switch / Application |
| IP Address | validated IPv4 format |
| Operating System | free text |
| Owner/Department | free text |
| Risk Level | Low / Medium / High / Critical |
| Security Status | Secure / Warning / Vulnerable |

## Requirements

- Python 3.7+
- No external libraries — uses only the standard library (`json`, `os`, `re`)

## How to Run

```bash
cd src
python3 asset_inventory.py
```

The app loads existing assets from `data/assets.json` on startup (three
sample assets are pre-loaded — A101, A102, A103 — matching the assignment's
sample data) and saves back to that file after every add, update, or delete.

## Sample Output

Running **Display All Assets** on the pre-loaded data produces:

```
=========================================
 CYBERSECURITY ASSET INVENTORY
=========================================
Asset ID : A101
Asset Name : HR-PC-01
Asset Type : Workstation
IP Address : 192.168.1.10
OS : Windows 11
Department : HR
Risk Level : Medium
Status : Secure
-----------------------------------------
Asset ID : A102
Asset Name : Web-Server
Asset Type : Server
IP Address : 192.168.1.20
OS : Ubuntu
Department : IT
Risk Level : Critical
Status : Vulnerable
-----------------------------------------
Asset ID : A103
Asset Name : Core-Router
Asset Type : Router
IP Address : 192.168.1.1
OS : Cisco IOS
Department : Network
Risk Level : High
Status : Warning
=========================================
Total Assets : 3
Critical Assets : 1
High Risk Assets : 1
Medium Risk Assets : 1
Vulnerable Assets : 1
=========================================
```

## Repository Structure

```
Week-01-Cybersecurity-Asset-Inventory/
│
├── src/
│   └── asset_inventory.py
│
├── data/
│   └── assets.json
│
├── tests/
│   └── test_cases.md
│
├── screenshots/
│   ├── 01-add-asset.png
│   ├── 02-display-assets.png
│   ├── 03-search-asset.png
│   ├── 04-update-asset.png
│   ├── 05-delete-asset.png
│   ├── 06-security-summary.png
│   └── 07-input-validation.png
│
└── README.md
```

> The `screenshots/` images aren't included here — capture them by running
> `asset_inventory.py` yourself and screenshotting each menu operation (see
> `tests/test_cases.md` for the exact steps to trigger each one, including
> the invalid-input case for `07-input-validation.png`).
