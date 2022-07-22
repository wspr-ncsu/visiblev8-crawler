const { URL } = require('url');
const puppeteer = require('puppeteer');
const crypto = require('crypto')
const PuppeteerHar = require('puppeteer-har');

// Tuning parameters
const DEFAULT_LOITER_TIME = 15.0;
 
// CLI entry point
function main() {
    const program = require('commander');
    program
        .version('1.0.0');
    program
        .command("visit <URL>")
        .description("Visit the given URL, creating a page record and collecting all data")
        .action(async function(input_url) {
            console.log(input_url);
            const browser = await puppeteer.launch({
                headless: true,
                executablePath: '/opt/chromium.org/chromium/chrome',
                args: [
                    "--disable-gpu",
                    "--disable-setuid-sandbox",
                    "--no-sandbox",
                ]
            });

            const page = await browser.newPage();
            const har = new PuppeteerHar(page);
            const url = new URL(input_url);
            let filename = crypto.createHash('sha256').update(input_url).digest('hex');
            try {
                await har.start({ path: `${filename}.har` });
                await page.goto(url, {
                    timeout: DEFAULT_LOITER_TIME * 1000,
                    waitUntil: 'networkidle0'
                });
                await logo.screenshot({path: `./${filename}.png`});
                

            } catch (ex) {
                console.error(ex);
            }
            await har.stop()
            await page.close();
            await browser.close();
            
        });
    program.parse(process.argv);
}

main();
