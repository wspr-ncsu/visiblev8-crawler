const { URL } = require('url');
const puppeteer = require('puppeteer-extra');
const PuppeteerHar = require('puppeteer-har');
const { TimeoutError } = require('puppeteer-core');
const PuppeteerExtraPluginStealth = require('puppeteer-extra-plugin-stealth');
const fs = require( 'fs' );
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
                    //' --enable-logging=stderr',
                    '--enable-automation',
                    //'--v=1'
                ];
    const crawler_args = process.argv.slice(5);

    program
        .version('1.0.0');
    program
        .command("visit <URL> <uid>")
        .option( '--headless <headless>', 'Which headless mode to run visiblev8', 'new')
        .option( '--loiter-time <loiter_time>', 'Amount of time to loiter on a webpage', DEFAULT_LOITER_TIME)
        .option( '--nav-time <nav_time>', 'Amount of time to wait for a page to load', DEFAULT_NAV_TIME)
        .allowUnknownOption(true)
        .description("Visit the given URL and store it under the UID, creating a page record and collecting all data")
        .action(async function(input_url, uid, options) {
            let combined_crawler_args = default_crawler_args.concat(crawler_args);
            let show_log = false;
            const user_data_dir = `/tmp/${uid}`;

            if ( combined_crawler_args.includes( '--show-chrome-log' ) ) {
                show_log = true;
                combined_crawler_args = combined_crawler_args.filter( function( item ) {
                    return item !== '--show-chrome-log';
                } );
            }

            console.log(combined_crawler_args)

            if ( combined_crawler_args.includes( '--no-headless' ) ) {
                options.headless = false;
                combined_crawler_args = combined_crawler_args.filter( function( item ) {
                    return item !== '--no-headless';
                } );
            }

            if ( combined_crawler_args.includes( '--no-screenshot' ) ) {
                options.disable_screenshots = true;
                combined_crawler_args = combined_crawler_args.filter( function( item ) {
                    return item !== '--no-screenshot';
                } );
            }

            console.log('no-headless: ', options.headless);

            puppeteer.use(PuppeteerExtraPluginStealth());
            const browser = await puppeteer.launch({
                headless: options.headless,
                userDataDir: user_data_dir,
                dumpio: show_log,
                executablePath: '/opt/chromium.org/chromium/chrome',
                args: combined_crawler_args,
                timeout: 60 * 1000,
                protocolTimeout: 60 * 1000,
            });

            const page = await browser.newPage( { viewport: null } );
            const har = new PuppeteerHar(page);
            const url = new URL(input_url);
            try {
                await har.start({ path: `${uid}.har` });
                try{
                    await page.goto(url, {
                        timeout: options.navTime * 1000,
                        waitUntil: 'networkidle0'
                    });
                } catch (ex) {
                    if ( ex instanceof TimeoutError ) {
                        await sleep(options.loiterTime * 1000);
                    } else {
                        throw ex;
                    }
                } finally {
                    await sleep(options.loiterTime * 1000);
                }
                if ( !options.disable_screenshots )
                    await page.screenshot({path: `./${uid}.png`});
                

            } catch (ex) {
                console.error(ex);
                process.exitCode = -1;
            }
            await har.stop()
            await page.close();
            await browser.close();
            console.log(`Finished crawling, ${url} cleaning up...`);
            // Throw away user data
            await fs.promises.rm(user_data_dir, { recursive: true, force: true });
            
        });
    program.parse(process.argv);
}

main();
