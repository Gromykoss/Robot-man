import { chromium } from 'playwright';
import { writeFileSync } from 'fs';

async function main() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  page.setDefaultTimeout(30000);

  // Go to Hydrogen/GULAG login
  await page.goto('https://spacegulag.online/hydrogen/', { waitUntil: 'networkidle' });
  console.log('Page loaded');

  // Wait for the inject to run
  await page.waitForTimeout(3000);

  // Log in with test user credentials
  const serverInput = page.locator('input#homeserver, input[placeholder*="сервер"]');
  const usernameInput = page.locator('input#username, input[placeholder*="номер"]');
  const passwordInput = page.locator('input#password, input[placeholder*="пароль"] input[type="password"]');

  // Try to find the login form
  await page.waitForTimeout(2000);

  // Take a screenshot at the login page to see what we have
  await page.screenshot({ path: '/tmp/gulag-login.png' });
  console.log('Login screenshot taken');

  // Fill in credentials  
  const hs = page.locator('#homeserver');
  const un = page.locator('#username');
  const pw = page.locator('#password');

  if (await hs.isVisible()) {
    await hs.fill('spacegulag.online');
    await un.fill('gromykoss');
    await pw.fill('Gromykoss1306!');
    
    // Click login button
    const loginBtn = page.locator('button.button-action.primary, button:has-text("ВОЙТИ")');
    await loginBtn.click();
    console.log('Login clicked');
  } else {
    // Try SSO or other layout
    console.log('Could not find standard login fields, trying alternative...');
    const inputs = await page.locator('input').all();
    console.log(`Found ${inputs.length} inputs`);
    for (const inp of inputs) {
      const ph = await inp.getAttribute('placeholder');
      console.log(`  input placeholder: ${ph}`);
    }
  }

  // Wait for room list to load
  await page.waitForTimeout(8000);
  await page.screenshot({ path: '/tmp/gulag-after-login.png' });
  console.log('After login screenshot taken');

  // Find and click a room in the room list (КПЗ or any available room)
  const rooms = page.locator('.RoomList a, .room-item, [class*="room"]');
  const roomCount = await rooms.count();
  console.log(`Found ${roomCount} room elements`);

  if (roomCount > 0) {
    // Click first room
    await rooms.first().click();
    await page.waitForTimeout(3000);
    console.log('Room clicked');
  }

  // Click the room-options button (👥)
  const roomOptions = page.locator('.room-options');
  if (await roomOptions.isVisible({ timeout: 5000 }).catch(() => false)) {
    await roomOptions.click();
    await page.waitForTimeout(2000);
    console.log('Room options clicked — member popup should appear');
  } else {
    console.log('Room options button not found, taking screenshot');
  }

  await page.screenshot({ path: '/tmp/gulag-member-popup.png' });
  console.log('Member popup screenshot taken');

  // Check if our popup appeared
  const popup = page.locator('.gulag-member-popup');
  if (await popup.isVisible({ timeout: 3000 }).catch(() => false)) {
    console.log('✅ GULAG member popup IS visible');
    
    // Check for delete buttons
    const delBtns = popup.locator('button:has-text("✕")');
    const delCount = await delBtns.count();
    console.log(`Found ${delCount} delete (✕) buttons`);
    
    // Check for search input
    const searchInput = popup.locator('input[placeholder*="username"]');
    console.log(`Search input visible: ${await searchInput.isVisible().catch(() => false)}`);
    
    // Check for ADD button
    const addBtn = popup.locator('button:has-text("ДОБАВИТЬ")');
    console.log(`Add button visible: ${await addBtn.isVisible().catch(() => false)}`);
    
    // Check for invite link button
    const linkBtn = popup.locator('button:has-text("ССЫЛКА")');
    console.log(`Invite link button visible: ${await linkBtn.isVisible().catch(() => false)}`);
    
    // Close popup
    const closeBtn = popup.locator('span:has-text("✕")').last();
    if (await closeBtn.isVisible().catch(() => false)) {
      await closeBtn.click();
      console.log('Popup closed via ✕');
    }
  } else {
    console.log('❌ GULAG member popup NOT visible');
  }

  await page.waitForTimeout(1000);
  await browser.close();
  console.log('Done');
}

main().catch(e => {
  console.error('ERROR:', e.message);
  process.exit(1);
});
