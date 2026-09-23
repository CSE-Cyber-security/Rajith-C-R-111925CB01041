# Test Cases – Cybersecurity Asset Inventory System

These are manual test cases to run against `src/asset_inventory.py`.
For each, note the menu option used, the inputs, and whether the actual
result matched the expected result.

| # | Feature | Steps | Input | Expected Result |
|---|---------|-------|-------|------------------|
| 1 | Display seed data | Menu → `2` | — | Shows A101, A102, A103 exactly as in the assignment's *Expected Output*, plus `Total Assets: 3`, `Critical Assets: 1`, `High Risk Assets: 1`, `Medium Risk Assets: 1`, `Vulnerable Assets: 1` |
| 2 | Add valid asset | Menu → `1` | ID `A104`, Name `DB-Server`, Type `Application`, IP `10.0.0.5`, OS `CentOS`, Dept `Finance`, Risk `High`, Status `Secure` | Asset added, confirmation message shown, `data/assets.json` now has 4 assets |
| 3 | Add with duplicate ID | Menu → `1`, use an ID that already exists (e.g. `A101`) | — | Rejected with "already exists" message, no duplicate created |
| 4 | Add with invalid Asset Type | Menu → `1`, type `Server-Rack` when asked for Asset Type | — | Re-prompted until a valid type (Workstation/Server/Router/Switch/Application) is entered |
| 5 | Add with invalid Risk Level | Menu → `1`, type `Extreme` when asked for Risk Level | — | Re-prompted until one of Low/Medium/High/Critical is entered |
| 6 | Add with invalid IP address | Menu → `1`, type `999.1.1.1` or `notanip` for IP Address | — | Rejected as invalid, re-prompted until a valid dotted IPv4 address is entered |
| 7 | Search existing asset | Menu → `3` | ID `A102` | Full details for Web-Server (Server, Critical, Vulnerable) are printed |
| 8 | Search non-existent asset | Menu → `3` | ID `Z999` | "No asset found with ID 'Z999'." |
| 9 | Update existing asset (partial) | Menu → `4`, ID `A103`, only change Risk Level to `Critical`, leave everything else blank | — | Only `risk_level` changes to `Critical`; all other fields (name, IP, OS, etc.) stay the same |
| 10 | Update non-existent asset | Menu → `4` | ID `Z999` | "No asset found with ID 'Z999'." |
| 11 | Update with invalid value | Menu → `4`, ID `A101`, enter `Huge` for Risk Level | — | Update to that field is rejected, previous value is kept, other valid edits still apply |
| 12 | Delete existing asset (confirm) | Menu → `5`, ID `A104`, confirm with `y` | — | Asset removed from inventory and from `data/assets.json` |
| 13 | Delete existing asset (cancel) | Menu → `5`, ID `A101`, answer `n` at confirmation | — | Asset is **not** deleted, "Deletion cancelled." shown |
| 14 | Delete non-existent asset | Menu → `5` | ID `Z999` | "No asset found with ID 'Z999'." |
| 15 | Security summary | Menu → `6` | — | Shows counts by Risk Level (Low/Medium/High/Critical) and by Security Status (Secure/Warning/Vulnerable), plus a list of assets flagged as Critical risk or Vulnerable status |
| 16 | Invalid menu choice | At main menu, enter `9` | — | "Invalid choice. Please enter a number from 1-7." then menu re-displays |
| 17 | Empty required field | Menu → `1`, press Enter with no text for Asset Name | — | Re-prompted, since empty values are rejected for required text fields |
| 18 | Persistence across runs | Add an asset, exit (`7`), relaunch the script, Display All (`2`) | — | Newly added asset is still present — confirms data was saved to `data/assets.json` |

## How to run

```bash
cd src
python3 asset_inventory.py
```

Take a screenshot after each test case that corresponds to one of the
required screenshots in `screenshots/` (add, display, search, update,
delete, security summary, and input validation).
