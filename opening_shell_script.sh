#!/bin/bash
# Start Chrome instances with specific debugging ports and user data directories
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium_chrome_profile" &
sleep 5
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9333 --user-data-dir="C:\selenium_chrome_profile_2" &

# Wait for a few seconds to ensure Chrome instances are up
sleep 5

