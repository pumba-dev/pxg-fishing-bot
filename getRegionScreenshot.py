import pyautogui

def getRegionScreenshot(region):
    #Get the screenshot of the region
    screenshot = pyautogui.screenshot(region=region)
    #Save the screenshot
    screenshot.save("regionScreenshot.png")

getRegionScreenshot((1692, 0, 214, 1080))