const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new'
  });

  const page = await browser.newPage();

  // Set viewport to match the card size
  await page.setViewport({
    width: 720,
    height: 720,
    deviceScaleFactor: 2
  });

  // Navigate to the HTML file
  const htmlPath = path.join(__dirname, 'card_v1.html');
  await page.goto(`file://${htmlPath}`, {
    waitUntil: 'networkidle0'
  });

  // Wait a bit for fonts to load
  await page.waitForTimeout(1000);

  // Take screenshot
  await page.screenshot({
    path: path.join(__dirname, 'outputs', 'output_v1.png'),
    fullPage: false
  });

  console.log('Screenshot saved to outputs/output_v1.png');

  await browser.close();
})();
