const { URL } = require('url');
const puppeteer = require('puppeteer-extra');
const PuppeteerHar = require('puppeteer-har');
const PuppeteerExtraPluginStealth = require('puppeteer-extra-plugin-stealth');
const fs = require( 'fs' )

// Tuning parameters
// Per Juestock et al. 30s + 15s for page load
const DEFAULT_NAV_TIME = 45;
const DEFAULT_LOITER_TIME = 15;

const sleep = ms => new Promise(r => setTimeout(r, ms));
 
// CLI entry point
function main() {
    const program = require('commander');

    const default_crawler_args = [
                    "--disable-setuid-sandbox",
                    "--no-sandbox",
                ];
    const crawler_args = process.argv.slice(6);

    program
        .version('1.0.0');
    program
        .command("visit <URL> <uid>")
        .option( '--headless <headless>', 'Run in headless mode', 'new')
        .option( '--loiter-time <loiter_time>', 'Amount of time to loiter on a webpage', DEFAULT_LOITER_TIME)
        .option( '--nav-time <nav_time>', 'Amount of time to wait for a page to load', DEFAULT_NAV_TIME)
        .allowUnknownOption(true)
        .description("Visit the given URL and store it under the UID, creating a page record and collecting all data")
        .action(async function(input_url, uid, headless, loiter_time, nav_time) {
            let combined_crawler_args = default_crawler_args.concat(crawler_args);

            puppeteer.use(PuppeteerExtraPluginStealth());
            const browser = await puppeteer.launch({
                headless: headless,
                userDataDir: `/tmp/${uid}`,
                executablePath: '/opt/chromium.org/chromium/chrome',
                args: combined_crawler_args
            });

            const page = await browser.newPage();
            const har = new PuppeteerHar(page);
            const url = new URL(input_url);
            try {
                await har.start({ path: `${uid}.har` });
                await page.goto(url, {
                    timeout: nav_time * 1000,
                    waitUntil: 'networkidle0'
                });

                await sleep(loiter_time * 1000);

                await page.screenshot({path: `./${uid}.png`});
                

            } catch (ex) {
                console.error(ex);
                process.exitCode = -1;
            }
            await har.stop()
            await page.close();
            await browser.close();
            // Throw away user data
            await fs.promises.rmdir(`/tmp/${uid}`, { recursive: true, force: true });
            
        });
    program.parse(process.argv);
}

main();
