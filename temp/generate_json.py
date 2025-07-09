import os
import json
from faker import Faker
import random

faker = Faker()

# Predefined issues
issues = [
  {
    "title": "Error 1603 during software installation",
    "description": "User encounters Error 1603 while installing a custom CRM tool. The installation fails midway with a generic fatal error.",
    "resolution": "1. Reviewed MSI installation logs and identified conflict with an older version.\n2. Uninstalled the older version using the vendor uninstaller.\n3. Removed leftover registry keys and files manually.\n4. Restarted the system and re-ran the installer as administrator.\n5. Installation completed successfully without errors.",
    "category": "Software Installation",
    "priority": "High"
  },
  {
    "title": "Office 365 installation stuck at 90%",
    "description": "Office 365 installer on user’s machine consistently halts at 90% progress. Task manager shows minimal activity.",
    "resolution": "1. Terminated the 'OfficeClickToRun.exe' process.\n2. Ran SaRA (Support and Recovery Assistant) to clean up incomplete install files.\n3. Cleared Office registry entries.\n4. Downloaded and executed the offline Office installer.\n5. Installation completed in 15 minutes.",
    "category": "Software Installation",
    "priority": "High"
  },
  {
    "title": "Adobe Acrobat fails due to missing DLL",
    "description": "Adobe Acrobat installation fails with 'VCRUNTIME140.dll is missing' error on startup after install.",
    "resolution": "1. Installed latest Visual C++ Redistributables (x86 and x64).\n2. Rebooted the system.\n3. Verified DLL presence in `System32` folder.\n4. Re-ran the Adobe installer and activated the product successfully.",
    "category": "Software Installation",
    "priority": "High"
  },
  {
    "title": "Installer blocked by company antivirus",
    "description": "User reports that Trend Micro antivirus quarantines an installer file needed for internal testing.",
    "resolution": "1. Confirmed SHA256 hash of installer matched original provided by vendor.\n2. Requested exception from InfoSec team.\n3. Whitelisted application for that device group.\n4. Installer executed normally and software was operational.",
    "category": "Software Installation",
    "priority": "Medium"
  },
  {
    "title": "Software not visible in Control Panel",
    "description": "User claims software is installed but it's not listed in Control Panel > Programs and Features.",
    "resolution": "1. Confirmed presence of files in Program Files.\n2. Verified installation path and missing uninstall string in registry.\n3. Reinstalled the application to restore proper registry entries.\n4. Verified it's now visible in the uninstall list.",
    "category": "Software Installation",
    "priority": "Low"
  },
  {
    "title": "Installation blocked by AppLocker policy",
    "description": "Installer for third-party plugin fails due to an AppLocker GPO policy enforced by the organization.",
    "resolution": "1. Collected AppLocker logs via Event Viewer.\n2. Identified the software’s digital signature as blocked.\n3. Submitted software details for whitelisting.\n4. After approval, updated AppLocker rules via GPO.\n5. Installer executed successfully.",
    "category": "Software Installation",
    "priority": "High"
  },
  {
    "title": "Setup requires .NET Framework 3.5",
    "description": "Legacy payroll application installer shows error requiring .NET 3.5 which isn’t enabled by default.",
    "resolution": "1. Enabled .NET Framework 3.5 using DISM command.\n2. Mounted local ISO as a source if internet download failed.\n3. Post-install, verified version with `dotnet --list-runtimes`.\n4. Installed the legacy app successfully.",
    "category": "Software Installation",
    "priority": "Medium"
  },
  {
    "title": "Installer closes without message",
    "description": "Upon double-clicking the installer, it immediately closes without any errors shown.",
    "resolution": "1. Ran installer via Command Prompt to capture stdout/stderr.\n2. Detected dependency on Windows Installer Service.\n3. Restarted Windows Installer service and re-ran setup.\n4. Software installed properly.",
    "category": "Software Installation",
    "priority": "Low"
  },
  {
    "title": "Conflicting version already installed",
    "description": "User tries to install SAP Client version 7.5, but installer throws 'newer version detected' warning.",
    "resolution": "1. Used SAP’s cleanup utility to remove residual registry entries.\n2. Uninstalled related dependencies (Java runtime).\n3. Clean booted the system.\n4. Performed a clean install of version 7.5.",
    "category": "Software Installation",
    "priority": "Medium"
  },
  {
    "title": "Autodesk license service not installed",
    "description": "After AutoCAD installation, user is unable to launch it due to license service error.",
    "resolution": "1. Checked if 'Autodesk Desktop Licensing Service' was running.\n2. Service was missing — manually installed it from Autodesk support package.\n3. Restarted PC and verified product activation.",
    "category": "Software Installation",
    "priority": "High"
  },
  {
    "title": "User denied admin rights to install IDE",
    "description": "User tried to install Visual Studio Code but was denied due to non-admin privileges.",
    "resolution": "1. Provided portable (zip) version of VS Code which does not require installation.\n2. Placed it in user’s profile directory.\n3. Added user extensions manually.\n4. Configured auto-launch using registry key.",
    "category": "Software Installation",
    "priority": "Low"
  },
  {
    "title": "Installer fails on Windows 11",
    "description": "Installer designed for Windows 10 fails silently on newly provisioned Windows 11 laptops.",
    "resolution": "1. Contacted vendor for updated Windows 11 compatible version.\n2. Confirmed backward compatibility issue.\n3. Ran installer in compatibility mode (Windows 10).\n4. Completed installation successfully.",
    "category": "Software Installation",
    "priority": "High"
  },
  {
    "title": "Installer requires Java runtime",
    "description": "Application installer throws error: 'Java not found on system'.",
    "resolution": "1. Installed latest Java SE Runtime Environment.\n2. Set `JAVA_HOME` environment variable.\n3. Added Java `bin` folder to PATH.\n4. Installer detected Java correctly and completed.",
    "category": "Software Installation",
    "priority": "Medium"
  },
  {
    "title": "Application fails silent install via script",
    "description": "Bulk deployment of PDF reader via script fails silently on some endpoints.",
    "resolution": "1. Enabled verbose logging with `/L*v install.log` switch.\n2. Found that script was not running with elevated privileges.\n3. Modified deployment script to use SCCM with system context.\n4. All endpoints received software successfully.",
    "category": "Software Installation",
    "priority": "High"
  },
  {
    "title": "Installer cannot connect to internet",
    "description": "User running installer receives 'Unable to connect to server' error during setup.",
    "resolution": "1. Checked firewall and proxy settings.\n2. Added installer domain to proxy allowlist.\n3. Temporarily disabled endpoint protection.\n4. Completed installation.\n5. Re-enabled protections post-install.",
    "category": "Software Installation",
    "priority": "High"
  },
  {
    "title": "Licensing activation fails post-install",
    "description": "Software installs successfully but activation fails due to invalid license server communication.",
    "resolution": "1. Verified license key is valid and unused.\n2. Ensured license server ports (TCP 27000-27010) are open.\n3. Added exception in firewall.\n4. Software successfully activated after retry.",
    "category": "Software Installation",
    "priority": "High"
  },
  {
    "title": "Installer stuck on 'Preparing to install'",
    "description": "User reports software setup freezes indefinitely at the initial loading screen.",
    "resolution": "1. Cleared `%TEMP%` directory.\n2. Disabled all startup items using `msconfig`.\n3. Performed clean boot and reran setup.\n4. Installation completed in less than 5 minutes.",
    "category": "Software Installation",
    "priority": "Medium"
  },
  {
    "title": "Installer fails due to Group Policy settings",
    "description": "Setup blocked due to policy: 'Only signed applications may run'.",
    "resolution": "1. Checked local group policies applied to the machine.\n2. Temporarily moved user to unrestricted OU.\n3. Completed installation successfully.\n4. Moved device back and verified GPO restored.",
    "category": "Software Installation",
    "priority": "High"
  },
  {
    "title": "Installer exits with error code -2147023293",
    "description": "Installer for graphics driver returns error -2147023293 without UI error message.",
    "resolution": "1. Researched error — found to be related to Windows Installer corruption.\n2. Ran `sfc /scannow` and DISM scan to repair Windows.\n3. Restarted and re-ran installer successfully.\n4. Updated driver version validated post-reboot.",
    "category": "Software Installation",
    "priority": "High"
  },
  {
    "title": "User accidentally installed wrong language pack",
    "description": "User installed French version of software instead of English by mistake.",
    "resolution": "1. Uninstalled the French version.\n2. Removed related language pack entries from registry.\n3. Cleared installer cache folders.\n4. Reinstalled English version and locked language setting in GPO.",
    "category": "Software Installation",
    "priority": "Low"
  }
]



# File path
json_path = "realistic_it_helpdesk_tickets.json"

# Load existing data if file exists
if os.path.exists(json_path):
    with open(json_path, "r") as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []
else:
    existing_data = []

# Generate new entries
start_id = 1000 + len(existing_data)
for i in range(400):
    issue = random.choice(issues)
    existing_data.append({
        "ticket_id": f"INC{start_id + i}",
        "title": issue["title"],
        "description": issue["description"] + " " + faker.paragraph(nb_sentences=3),
        "resolution": issue["resolution"],
        "category": issue["category"],
        "priority": issue["priority"]
    })

# Save updated dataset
with open(json_path, "w") as f:
    json.dump(existing_data, f, indent=2)

print(f"Updated {json_path} with {len(existing_data)} total entries.")
