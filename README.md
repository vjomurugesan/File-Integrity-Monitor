# File-Integrity-Monitor
🛡️ File Integrity Monitor
A Python application that detects file modifications using SHA-256 hashing. It provides a graphical interface built with Tkinter to monitor file integrity in real time.
✨ Features
•	Select files to monitor.
•	Generate and register SHA-256 hashes.
•	Automatically check file integrity every 5 seconds.
•	Detect file modifications and display security alerts.
•	Display current status, hash values, and activity logs.
🛠️ Technologies Used
•	Python
•	Tkinter
•	hashlib
•	os
•	datetime
⚙️ How to Run
1.	Install Python 3.
2.	Clone or download this repository.
3.	Open the project folder in VS Code.
4.	Run the following command:
python file_integrity_monitor.py
🚀 How to Use
1.	Click Select File.
2.	Click Register Original Hash.
3.	Click Start Monitoring.
4.	View integrity checks and alerts in the application.
🔐 How It Works
The application calculates a file's SHA-256 hash and compares it with the registered original hash. If the hashes differ, a possible modification is detected and an alert is displayed.
⚠️ Note
Keep stored_hash.txt protected. If someone can modify both the monitored file and its stored baseline, unauthorized changes may go undetected.
👨‍💻 Purpose
Developed as a cybersecurity learning project to demonstrate file integrity monitoring and cryptographic hashing.
