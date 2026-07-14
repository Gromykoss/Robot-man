import asyncio
from playwright.async_api import async_playwright

async def is_visible(locator, timeout=3000):
    try:
        return await locator.is_visible(timeout=timeout)
    except:
        return False

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(40000)

        # Go to Hydrogengulag
        await page.goto('https://spacegulag.online/hydrogen/', wait_until='networkidle')
        print('✅ Page loaded')
        await page.wait_for_timeout(3000)

        # Take login screenshot
        await page.screenshot(path='/tmp/gulag-login.png')
        print('📸 Login page screenshot saved')

        # Fill login form
        try:
            await page.fill('#homeserver', 'spacegulag.online')
            print('✅ Filled homeserver')
        except Exception as e:
            print(f'❌ Could not fill homeserver: {e}')

        try:
            await page.fill('#username', 'gromykoss')
            print('✅ Filled username')
        except Exception as e:
            print(f'❌ Could not fill username: {e}')

        try:
            await page.fill('#password', 'Gromykoss1306!')
            print('✅ Filled password')
        except Exception as e:
            print(f'❌ Could not fill password: {e}')

        # Click login
        try:
            login_btn = page.locator('button:has-text("ВОЙТИ")')
            if await is_visible(login_btn):
                await login_btn.click()
                print('✅ Login clicked')
            else:
                print('❌ Login button not found')
        except Exception as e:
            print(f'❌ Login error: {e}')

        # Wait for rooms to load
        await page.wait_for_timeout(10000)
        await page.screenshot(path='/tmp/gulag-after-login.png')
        print('📸 After-login screenshot saved')

        # Find and click a room
        any_room = page.locator('.room-item, .RoomList a, .room-list-item, [class*="room-title"], [class*="room-name"]')
        ac = await any_room.count()
        print(f'Room selectors found: {ac}')
        
        if ac > 0:
            await any_room.first().click()
            await page.wait_for_timeout(3000)
            print('✅ Room clicked')

        # Click room-options button
        room_ops = page.locator('.room-options')
        ro_visible = await is_visible(room_ops)
        print(f'Room-options visible: {ro_visible}')

        if ro_visible:
            await room_ops.click()
            await page.wait_for_timeout(2000)
            print('✅ Room-options clicked')
        else:
            # Try by title/aria-label
            alt_ops = page.locator('[title*="room" i], [aria-label*="room" i], [class*="options"], [class*="RoomOptions"]')
            ao = await alt_ops.count()
            print(f'Alternative options buttons: {ao}')
            for i in range(ao):
                cls = await alt_ops.nth(i).get_attribute("class")
                print(f'  Button {i}: class="{cls}"')

        await page.screenshot(path='/tmp/gulag-member-popup.png')
        print('📸 After click screenshot saved')

        # Check if our popup is visible
        popup = page.locator('.gulag-member-popup')
        popup_visible = await is_visible(popup)
        if popup_visible:
            print('✅✅ GULAG member popup IS visible')
            
            popup_html = await popup.inner_html()
            print(f'Popup inner HTML (first 500 chars): {popup_html[:500]}')
            
            # Check all expected elements
            del_btns = page.locator('.gulag-member-popup button')
            del_count = await del_btns.count()
            print(f'  Buttons in popup: {del_count}')
            
            search_vis = await is_visible(page.locator('input[placeholder*="username"]'))
            print(f'  Search input visible: {search_vis}')
            
            add_vis = await is_visible(page.locator('button:has-text("ДОБАВИТЬ")'))
            print(f'  ДОБАВИТЬ button visible: {add_vis}')
            
            link_vis = await is_visible(page.locator('button:has-text("ССЫЛКА")'))
            print(f'  ССЫЛКА-ПРИГЛАШЕНИЕ button visible: {link_vis}')
            
            # Check for delete ✕ buttons
            del_x = page.locator('.gulag-member-popup button:has-text("✕")')
            dx_count = await del_x.count()
            print(f'  ✕ delete buttons: {dx_count}')
        else:
            print('❌ GULAG member popup NOT visible')
            body_text = await page.locator('body').text_content()
            print(f'Body text (first 1000 chars): {body_text[:1000]}')

        await browser.close()
        print('🏁 Done')

asyncio.run(main())
