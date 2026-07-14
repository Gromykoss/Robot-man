import asyncio
from playwright.async_api import async_playwright
import time

async def is_visible(locator, timeout=3000):
    try:
        return await locator.is_visible(timeout=timeout)
    except:
        return False

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(15000)

        # Go to GULAG
        await page.goto('https://spacegulag.online/hydrogen/', wait_until='networkidle')
        print('✅ Page loaded')
        await page.wait_for_timeout(4000)

        # Take screenshot of login
        await page.screenshot(path='/tmp/gulag-state-1.png')

        try:
            # Fill username
            await page.fill('input#username', 'gromykoss')
            print('✅ Filled username')
        except Exception as e:
            print(f'❌ Username fill error: {e}')

        await page.wait_for_timeout(200)

        try:
            # Fill password
            await page.fill('input#password', 'Gromykoss1306!')
            print('✅ Filled password')
        except Exception as e:
            print(f'❌ Password fill error: {e}')

        await page.wait_for_timeout(200)

        # Try clicking button
        try:
            btn = page.locator('button:has-text("ВОЙТИ")')
            if await is_visible(btn):
                await btn.click()
                print('✅ Login button clicked')
            else:
                # Try by class
                btn2 = page.locator('button.button-action.primary')
                if await is_visible(btn2):
                    await btn2.click()
                    print('✅ Login button (by class) clicked')
        except Exception as e:
            print(f'❌ Button click error: {e}')

        await page.wait_for_timeout(2000)

        # Try pressing Enter on password field
        try:
            await page.press('input#password', 'Enter')
            print('✅ Enter pressed on password')
        except Exception as e:
            print(f'❌ Enter error: {e}')

        # Wait for login to process
        for i in range(10):
            url = page.url
            if '/session' in url or '/room' in url:
                print(f'✅ Logged in! URL: {url}')
                break
            await page.wait_for_timeout(1000)
        else:
            print(f'⏱️ Still at login after 10s. URL: {page.url}')
            await page.screenshot(path='/tmp/gulag-login-fail.png')
            # Check for error message
            body = await page.locator('body').text_content() or ''
            if 'incorrect' in body.lower():
                print('❌ Login failed - incorrect credentials')

        if '/session' in page.url or '/room' in page.url:
            await page.wait_for_timeout(3000)
            await page.screenshot(path='/tmp/gulag-logged-in.png')
            
            # Try to find and click a room
            room_selectors = [
                '.RoomList a',
                '.room-item',
                '[class*="room-title"]',
                '[class*="room-name"]',
                '.LeftPanel a',
                'nav a',
            ]
            
            clicked = False
            for sel in room_selectors:
                loc = page.locator(sel)
                try:
                    count = await loc.count()
                    if count > 0:
                        await loc.first().click()
                        print(f'✅ Clicked room via {sel}')
                        clicked = True
                        break
                except:
                    continue
            
            if not clicked:
                print('⚠️ Could not find room to click')
            
            await page.wait_for_timeout(3000)
            
            # Click room-options button
            ro = page.locator('.room-options')
            if await is_visible(ro):
                await ro.click()
                await page.wait_for_timeout(1500)
                print('✅ Room-options clicked')
            
            await page.screenshot(path='/tmp/gulag-with-popup.png')
            
            # Check for popup
            popup = page.locator('.gulag-member-popup')
            if await is_visible(popup):
                print('✅✅ MEMBER POPUP IS VISIBLE!')
                html = await popup.inner_html()
                print(f'Popup HTML:\n{html[:2000]}')
            else:
                print('❌ Member popup not visible')
                # Debug what buttons exist
                btns = page.locator('button').all()
                for b in await btns:
                    txt = await b.text_content()
                    print(f'  Found button: "{txt}"')
        else:
            print('❌ Not logged in, skipping popup test')

        await browser.close()
        print('🏁 Done')

asyncio.run(main())
