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
        page.set_default_timeout(15000)

        await page.goto('https://spacegulag.online/hydrogen/', wait_until='networkidle')
        print('✅ Page loaded')
        await page.wait_for_timeout(3000)

        await page.fill('input#username', 'gromykoss')
        await page.fill('input#password', 'Gromykoss1306!')
        await page.wait_for_timeout(200)
        await page.locator('button:has-text("ВОЙТИ")').click()
        print('✅ Login clicked')

        for i in range(15):
            if '/session' in page.url:
                print(f'✅ Logged in! URL: {page.url}')
                break
            await page.wait_for_timeout(1000)
        else:
            print('⏱️ Still not logged in')

        if '/session' in page.url:
            await page.wait_for_timeout(3000)
            
            # Click КПЗ room
            kpz = page.locator('text=КПЗ').first
            if await is_visible(kpz):
                await kpz.click()
                print('✅ КПЗ room clicked')
                await page.wait_for_timeout(3000)
            else:
                print('❌ КПЗ not visible')
                # Try clicking first room link
                room_links = page.locator('.RoomList a').first
                if await is_visible(room_links, timeout=2000):
                    await room_links.click()
                    print('✅ First room link clicked')
                    await page.wait_for_timeout(3000)

            await page.screenshot(path='/tmp/gulag-in-room.png')

            # Find room-options button
            room_ops = page.locator('.room-options').first
            if await is_visible(room_ops, timeout=3000):
                await room_ops.click()
                print('✅ Room-options clicked')
                await page.wait_for_timeout(1500)
            else:
                print('❌ .room-options not found')
                # Print all buttons
                btns = page.locator('button')
                bc = await btns.count()
                print(f'Total buttons: {bc}')
                for i in range(bc):
                    cls = await btns.nth(i).get_attribute('class') or ''
                    text = await btns.nth(i).text_content() or ''
                    print(f'  Button {i}: class="{cls}" text="{text.strip()[:50]}"')

            await page.screenshot(path='/tmp/gulag-after-options-click.png')

            # Check popup
            popup = page.locator('.gulag-member-popup')
            if await is_visible(popup, timeout=3000):
                print('✅✅ MEMBER POPUP IS VISIBLE!')
                html = await popup.inner_html()
                print(f'Popup HTML:\n{html[:3000]}')
                
                # Check elements
                checks = [
                    ('search input', 'input[placeholder*="username"]'),
                    ('ДОБАВИТЬ button', 'button:has-text("ДОБАВИТЬ")'),
                    ('ССЫЛКА-ПРИГЛАШЕНИЕ button', 'button:has-text("ССЫЛКА")'),
                    ('✕ delete buttons', 'button:has-text("✕")'),
                ]
                for name, sel in checks:
                    loc = page.locator(sel).first
                    vis = await is_visible(loc, timeout=1000)
                    cnt = await page.locator(sel).count()
                    print(f'  {name}: visible={vis}, count={cnt}')
            else:
                print('❌ Member popup not visible')
                body = await page.locator('body').text_content() or ''
                print(f'Page body: {body[:500]}')

        await page.screenshot(path='/tmp/gulag-final-result.png')
        print('📸 Final screenshot saved')
        await browser.close()
        print('🏁 Done')

asyncio.run(main())
