import pyautogui

def getRegionScreenshot(region):
    #Get the screenshot of the region
    screenshot = pyautogui.screenshot(region=region)

    # parse to grayscale
    screenshot = screenshot.convert('L')

    #Save the screenshot
    screenshot.save("regionScreenshot.png")

getRegionScreenshot((50, 75, 50, 50))