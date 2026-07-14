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
        await page.wait_for_timeout(4000)

        # Debug: check what's visible on the page
        body_html = await page.locator('body').inner_html()
        # Find all inputs
        inputs = await page.locator('input').all()
        print(f'Found {len(inputs)} inputs:')
        for inp in inputs:
            id_attr = await inp.get_attribute('id')
            placeholder = await inp.get_attribute('placeholder')
            value = await inp.input_value()
            visible = await inp.is_visible()
            print(f'  id={id_attr}, placeholder="{placeholder}", value="{value}", visible={visible}')

        # Find all buttons
        buttons = await page.locator('button').all()
        print(f'Found {len(buttons)} buttons:')
        for btn in buttons:
            text = await btn.text_content()
            visible = await btn.is_visible()
            print(f'  text="{text.strip() if text else ""}", visible={visible}')

        # The server field already has a value, so just fill username and password
        # Clear and re-fill
        for inp in inputs:
            id_attr = await inp.get_attribute('id')
            if id_attr == 'homeserver':
                # Already filled with spacegulag.online, good
                pass
            elif id_attr == 'username':
                await inp.fill('gromykoss')
                print('✅ Filled username')
            elif id_attr == 'password':
                await inp.fill('Gromykoss1306!')
                print('✅ Filled password')

        await page.wait_for_timeout(500)

        # Try clicking the login button
        login_btn = page.locator('button:has-text("ВОЙТИ")')
        if await is_visible(login_btn):
            await login_btn.click()
            print('✅ Login clicked')
        else:
            print('❌ Login button not found')

        await page.wait_for_timeout(12000)
        await page.screenshot(path='/tmp/gulag-after-login2.png')
        print('📸 After login screenshot')

        # Check if we got past login
        url = page.url
        print(f'Current URL: {url}')
        body_text = await page.locator('body').text_content()
        if 'gromykoss' in body_text:
            print('Still on login page - login might have failed')
        
        # Try to find session/room elements
        session_view = page.locator('.SessionView')
        sv_visible = await is_visible(session_view)
        print(f'SessionView visible: {sv_visible}')

        left_panel = page.locator('.LeftPanel')
        lp_visible = await is_visible(left_panel)
        print(f'LeftPanel visible: {lp_visible}')

        # If logged in, click a room
        any_room = page.locator('.RoomList a, .room-item, [class*="room-title"], [class*="room-name"]')
        ac = await any_room.count()
        print(f'Room elements: {ac}')
        if ac > 0:
            await any_room.first().click()
            await page.wait_for_timeout(3000)
            print('✅ Room clicked')

        # Try room-options
        room_ops = page.locator('.room-options')
        ro_visible = await is_visible(room_ops)
        print(f'Room-options visible: {ro_visible}')
        if ro_visible:
            await room_ops.click()
            await page.wait_for_timeout(2000)

        await page.screenshot(path='/tmp/gulag-final.png')

        # Check popup
        popup = page.locator('.gulag-member-popup')
        popup_visible = await is_visible(popup)
        if popup_visible:
            print('✅✅ GULAG member popup IS visible')
            print(await popup.inner_html())
        else:
            print('❌ Popup not visible')
            # Print current URL
            print(f'Final URL: {page.url}')

        await browser.close()
        print('🏁 Done')

asyncio.run(main())
