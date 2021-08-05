class PageExtractors:
    '''
    Extractor class for locating and moving elements on Facebook feeds
    '''
    email_selector  = '//*[@id="email"]'
    passwd_selector = '//*[@id="pass"]'
    submit_selector = '//*[@type="submit"]'
    comments_block  = '//*[@aria-label="Leave a comment"]'
    body_height     = "return document.body.scrollHeight"
    scroll_body     = "window.scrollTo(0, document.body.scrollHeight);"
    comment_xpath   =  "//*[contains(@aria-label,'Comment by') or contains(@aria-label,'Reply by')]"
