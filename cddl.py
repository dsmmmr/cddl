# ------------------------------------------------------------------------------
# Set download path etc...
downLoadPath  = '/your/download/directory'
zugangsNummer = '012345678'

# ------------------------------------------------------------------------------
# Misc imports
from time import sleep
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager

# ------------------------------------------------------------------------------
# Login and goto postbox
def cddlLogin():

    # Prepare and open the chrome driver
    chromeOptions = Options()
    chromeOptions.add_experimental_option('prefs',  {
        "download.default_directory":         downLoadPath,
        "download.prompt_for_download":       False,
        "download.directory_upgrade":         True,
        "plugins.always_open_pdf_externally": True
        }
    )
    driver        = webdriver.Chrome('/usr/bin/chromedriver', options = chromeOptions)
    #driver        = webdriver.Chrome(ChromeDriverManager().install(), options = chromeOptions)
    comdirectUrl  = 'https://kunde.comdirect.de/lp/wt/login?execution=e1s1&afterTimeout=true'
    postBoxUrl    = 'https://kunde.comdirect.de/itx/posteingangsuche'
    driver.get(comdirectUrl);

    # Get the elements
    zugangsNummerField  = driver.find_element_by_name('param1')
    pinField            = driver.find_element_by_name('param3')
    loginButton         = driver.find_element_by_id('loginAction')
    
    # Click away the cookie button, maximum wait for 2 seconds
    tMaxCookie = 2
    t = 0
    while t <= tMaxCookie:
        try:
            cookieButton = driver.find_element_by_id('privacy-init-wall-button-accept')
            cookieButton.click()
            break
        except:
            print('Wait for cookie banner {:.1f} sec'.format(t))
            t = t + 0.1
            sleep(0.1)
    if t > tMaxCookie:
        print('No cookie banner found, continue anyway')
        print('')
        
    # Login
    zugangsNummerField.send_keys(zugangsNummer)
    pinField.send_keys(getpass('PIN: '))
    loginButton.click()
    sleep(1)

    # Goto postbox
    driver.get(postBoxUrl);

    # Wait for postbox
    cnt = 0
    while True:
        try:
            driver.find_element_by_link_text('Archiv')
            break
        except:
            cnt = cnt + 1
            print('Wait for postbox {:3d} sec'.format(cnt))
            sleep(1)

    return driver

# ------------------------------------------------------------------------------
# Download PDF files
def cddlGetPdf(driver):

    # Reset counters
    cntPdf  = 0
    cntHtml = 0
    page    = 0

    while True:

        page = page + 1
        print('----------------------------------------------')
        print('Downloading page {:d}'.format(page))
        print()

        # Scroll down to show the page number
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        sleep(1)

        # Get links and extract direct PDF-URLs from the links
        pdfLinks = driver.find_elements_by_css_selector("a[id*='urlAbfrage'][href*='.pdf']")
        pdfUrls  = []
        for pdfLink in pdfLinks:
            pdfUrls.append(pdfLink.get_attribute("href"))

        # Get the HTML links
        htmlLinks = driver.find_elements_by_css_selector("a[id*='urlAbfrage'][href*='.html']")
        htmlUrls  = []
        for htmlLink in htmlLinks:
            htmlUrls.append(htmlLink.get_attribute("href"))

        # Download all the PDFs to the default directory
        error = False
        for pdfUrl in pdfUrls:
            try:
                # Get short URL -> use part after last '/', use part before '?'
                pdfUrlShort = (pdfUrl.split('/')[-1]).split('?')[0]

                # Sometimes, Termingebundenes is .pdf despite being HTML -> check
                x = pdfUrl.split('Termingebundenes');
                if len(x) == 1:                         # Normal PDF download
                    cntPdf = cntPdf + 1
                    driver.get(pdfUrl)
                    sleep(0.3)
                    print('Get  {:4d}: {:s}'.format(cntPdf, pdfUrlShort))
                else:                                   # Skip possibly HTML
                    cntHtml = cntHtml + 1
                    print('Skip {:4d}: {:s}'.format(cntHtml, pdfUrlShort))
            except:
                driver.back()
                print('Error, failed to load {:s}'.format(pdfUrlShort))
                error = True
                break

        # Go to the next page
        if not error:

            # Show how many URLS were skipped
            for htmlUrl in htmlUrls:
                cntHtml = cntHtml + 1
                x = htmlUrl.split('/');
                htmlUrlShort = x[-1]
                print('Skip {:4d}: {:s}'.format(cntHtml, htmlUrlShort))
            print()

            # Check if there is another right button - stop if not
            try:
                rightbutton = driver.find_element_by_css_selector("a[id='f1-j_idt124_right']")
            except:
                print('----------------------------------------------')
                print('Downloaded -> {:5d} documents'.format(cntPdf))
                print('Skipped    -> {:5d} documents'.format(cntHtml))
                print('No more right button -> End of download')
                print('----------------------------------------------')
                break;
            driver.execute_script("arguments[0].click();", rightbutton)

        # Stop on error
        else:
            break

# ------------------------------------------------------------------------------
# Login and download
drv = cddlLogin()
cddlGetPdf(drv)

# ------------------------------------------------------------------------------
