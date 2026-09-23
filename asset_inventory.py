"""
Cybersecurity Asset Inventory System
Weekly Mini Project - 01

A menu-driven command-line application that lets a security administrator
add, search, update, delete, and display an organization's IT assets, and
view a summary of security risk across the inventory.

Run with:
    python asset_inventory.py
(from the src/ folder, or from anywhere - the data file path is resolved
relative to this script, so it always reads/writes ../data/assets.json)
"""

import json
import os
import re

# ---------------------------------------------------------------------------
# Configuration / constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(REPO_ROOT, "data", "assets.json")

ASSET_TYPES = ["Workstation", "Server", "Router", "Switch", "Application"]
RISK_LEVELS = ["Low", "Medium", "High", "Critical"]
SECURITY_STATUSES = ["Secure", "Warning", "Vulnerable"]

IP_PATTERN = re.compile(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$")

BAR_WIDTH = 41


# ---------------------------------------------------------------------------
# Core inventory class
# ---------------------------------------------------------------------------

class AssetInventory:
    """Holds the in-memory list of assets and handles persistence + CRUD."""

    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.assets = []
        self.load()

    # ---------- Persistence ----------

    def load(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    self.assets = json.load(f)
            except (json.JSONDecodeError, IOError):
                print("  Warning: could not read data file, starting empty.")
                self.assets = []
        else:
            self.assets = []

    def save(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, "w") as f:
            json.dump(self.assets, f, indent=2)

    # ---------- Validation helpers (these enforce input validation) ----------

    @staticmethod
    def _choose_from_list(prompt, options):
        """Keep asking until the user enters one of the allowed options."""
        options_display = "/".join(options)
        while True:
            value = input(f"{prompt} ({options_display}): ").strip()
            for option in options:
                if value.lower() == option.lower():
                    return option
            print(f"  Invalid value. Please choose one of: {options_display}")

    @staticmethod
    def _valid_ip(ip):
        match = IP_PATTERN.match(ip)
        if not match:
            return False
        return all(0 <= int(octet) <= 255 for octet in match.groups())

    def _input_ip(self, prompt="IP Address"):
        while True:
            ip = input(f"{prompt}: ").strip()
            if self._valid_ip(ip):
                return ip
            print("  Invalid IP address format. Example: 192.168.1.10")

    @staticmethod
    def _input_nonempty(prompt):
        while True:
            value = input(f"{prompt}: ").strip()
            if value:
                return value
            print("  This field cannot be empty.")

    def _asset_id_exists(self, asset_id):
        return any(a["asset_id"].lower() == asset_id.lower() for a in self.assets)

    def find_asset(self, asset_id):
        for asset in self.assets:
            if asset["asset_id"].lower() == asset_id.lower():
                return asset
        return None

    # ---------- Add ----------

    def add_asset(self):
        print("\n--- Add New Asset ---")
        asset_id = self._input_nonempty("Asset ID")
        if self._asset_id_exists(asset_id):
            print(f"  Asset ID '{asset_id}' already exists. Use Update instead.")
            return

        asset = {
            "asset_id": asset_id,
            "asset_name": self._input_nonempty("Asset Name"),
            "asset_type": self._choose_from_list("Asset Type", ASSET_TYPES),
            "ip_address": self._input_ip(),
            "os": self._input_nonempty("Operating System"),
            "department": self._input_nonempty("Owner/Department"),
            "risk_level": self._choose_from_list("Risk Level", RISK_LEVELS),
            "security_status": self._choose_from_list("Security Status", SECURITY_STATUSES),
        }
        self.assets.append(asset)
        self.save()
        print(f"  Asset '{asset_id}' added successfully.")

    # ---------- Search ----------

    def search_asset(self):
        print("\n--- Search Asset ---")
        asset_id = self._input_nonempty("Enter Asset ID to search")
        asset = self.find_asset(asset_id)
        if asset:
            print()
            self._print_asset(asset)
        else:
            print(f"  No asset found with ID '{asset_id}'.")

    # ---------- Update ----------

    def update_asset(self):
        print("\n--- Update Asset ---")
        asset_id = self._input_nonempty("Enter Asset ID to update")
        asset = self.find_asset(asset_id)
        if not asset:
            print(f"  No asset found with ID '{asset_id}'.")
            return

        print("  Current details (press Enter to keep a value unchanged):")
        self._print_asset(asset)
        print()

        name = input(f"Asset Name [{asset['asset_name']}]: ").strip()
        if name:
            asset["asset_name"] = name

        atype = input(f"Asset Type [{asset['asset_type']}] ({'/'.join(ASSET_TYPES)}): ").strip()
        if atype:
            match = next((o for o in ASSET_TYPES if o.lower() == atype.lower()), None)
            asset["asset_type"] = match if match else asset["asset_type"]
            if not match:
                print("  Invalid asset type, keeping previous value.")

        ip = input(f"IP Address [{asset['ip_address']}]: ").strip()
        if ip:
            if self._valid_ip(ip):
                asset["ip_address"] = ip
            else:
                print("  Invalid IP, keeping previous value.")

        os_val = input(f"Operating System [{asset['os']}]: ").strip()
        if os_val:
            asset["os"] = os_val

        dept = input(f"Owner/Department [{asset['department']}]: ").strip()
        if dept:
            asset["department"] = dept

        risk = input(f"Risk Level [{asset['risk_level']}] ({'/'.join(RISK_LEVELS)}): ").strip()
        if risk:
            match = next((o for o in RISK_LEVELS if o.lower() == risk.lower()), None)
            asset["risk_level"] = match if match else asset["risk_level"]
            if not match:
                print("  Invalid risk level, keeping previous value.")

        status = input(f"Security Status [{asset['security_status']}] ({'/'.join(SECURITY_STATUSES)}): ").strip()
        if status:
            match = next((o for o in SECURITY_STATUSES if o.lower() == status.lower()), None)
            asset["security_status"] = match if match else asset["security_status"]
            if not match:
                print("  Invalid security status, keeping previous value.")

        self.save()
        print(f"  Asset '{asset_id}' updated successfully.")

    # ---------- Delete ----------

    def delete_asset(self):
        print("\n--- Delete Asset ---")
        asset_id = self._input_nonempty("Enter Asset ID to delete")
        asset = self.find_asset(asset_id)
        if not asset:
            print(f"  No asset found with ID '{asset_id}'.")
            return

        self._print_asset(asset)
        confirm = input("Are you sure you want to delete this asset? (y/n): ").strip().lower()
        if confirm == "y":
            self.assets.remove(asset)
            self.save()
            print(f"  Asset '{asset_id}' deleted.")
        else:
            print("  Deletion cancelled.")

    # ---------- Display ----------

    @staticmethod
    def _print_asset(asset):
        print(f"Asset ID : {asset['asset_id']}")
        print(f"Asset Name : {asset['asset_name']}")
        print(f"Asset Type : {asset['asset_type']}")
        print(f"IP Address : {asset['ip_address']}")
        print(f"OS : {asset['os']}")
        print(f"Department : {asset['department']}")
        print(f"Risk Level : {asset['risk_level']}")
        print(f"Status : {asset['security_status']}")

    def _counts(self):
        total = len(self.assets)
        critical = sum(1 for a in self.assets if a["risk_level"] == "Critical")
        high = sum(1 for a in self.assets if a["risk_level"] == "High")
        medium = sum(1 for a in self.assets if a["risk_level"] == "Medium")
        vulnerable = sum(1 for a in self.assets if a["security_status"] == "Vulnerable")
        return total, critical, high, medium, vulnerable

    def display_all(self):
        print("\n" + "=" * BAR_WIDTH)
        print(" CYBERSECURITY ASSET INVENTORY")
        print("=" * BAR_WIDTH)

        if not self.assets:
            print("No assets in inventory.")
        else:
            for i, asset in enumerate(self.assets):
                self._print_asset(asset)
                if i < len(self.assets) - 1:
                    print("-" * BAR_WIDTH)

        print("=" * BAR_WIDTH)
        total, critical, high, medium, vulnerable = self._counts()
        print(f"Total Assets : {total}")
        print(f"Critical Assets : {critical}")
        print(f"High Risk Assets : {high}")
        print(f"Medium Risk Assets : {medium}")
        print(f"Vulnerable Assets : {vulnerable}")
        print("=" * BAR_WIDTH)

    # ---------- Security summary ----------

    def security_summary(self):
        print("\n" + "=" * BAR_WIDTH)
        print(" SECURITY SUMMARY")
        print("=" * BAR_WIDTH)

        total, critical, high, medium, vulnerable = self._counts()
        print(f"Total Assets : {total}")
        print("-" * BAR_WIDTH)

        print("By Risk Level:")
        for level in RISK_LEVELS:
            count = sum(1 for a in self.assets if a["risk_level"] == level)
            print(f"  {level:<9}: {count}")
        print("-" * BAR_WIDTH)

        print("By Security Status:")
        for status in SECURITY_STATUSES:
            count = sum(1 for a in self.assets if a["security_status"] == status)
            print(f"  {status:<9}: {count}")
        print("-" * BAR_WIDTH)

        attention = [
            a for a in self.assets
            if a["risk_level"] == "Critical" or a["security_status"] == "Vulnerable"
        ]
        if attention:
            print("Assets Requiring Immediate Attention:")
            for a in attention:
                print(f"  {a['asset_id']} - {a['asset_name']} "
                      f"({a['risk_level']} risk / {a['security_status']})")
        else:
            print("No assets currently require immediate attention.")
        print("=" * BAR_WIDTH)


# ---------------------------------------------------------------------------
# Menu / entry point
# ---------------------------------------------------------------------------

def print_menu():
    print("\n" + "-" * BAR_WIDTH)
    print(" CYBERSECURITY ASSET INVENTORY - MENU")
    print("-" * BAR_WIDTH)
    print("1. Add Asset")
    print("2. Display All Assets")
    print("3. Search Asset")
    print("4. Update Asset")
    print("5. Delete Asset")
    print("6. Security Summary")
    print("7. Exit")


def main():
    inventory = AssetInventory()
    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            inventory.add_asset()
        elif choice == "2":
            inventory.display_all()
        elif choice == "3":
            inventory.search_asset()
        elif choice == "4":
            inventory.update_asset()
        elif choice == "5":
            inventory.delete_asset()
        elif choice == "6":
            inventory.security_summary()
        elif choice == "7":
            print("Exiting. All changes have been saved. Goodbye!")
            break
        else:
            print("  Invalid choice. Please enter a number from 1-7.")


if __name__ == "__main__":
    main()
