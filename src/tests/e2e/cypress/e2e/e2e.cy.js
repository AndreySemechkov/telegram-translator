describe('App opens test', () => {
  it('should visit the page, check for network errors, and verify xhr request length', () => {
    cy.visit('https://stage-app.ironwatchers.com/')

    cy.window().then((win) => {
      cy.stub(win.console, 'error').callsFake((msg) => {
        if (msg.includes('Failed to load resource')) {
          throw new Error(`Network Error: ${msg}`)
        }
      })
    })

    // Intercept GET requests
    cy.intercept('GET', '**').as('xhr')

    // Wait for the intercepted GET request
    cy.wait('@xhr').then(({ request, response }) => {
      // Check the Content-Length header in the response (not the request)
      const contentLength = response.headers['content-length']
      expect(contentLength).to.not.equal('0')
    })
  })
})

describe('No 403 Responses Test', () => {
  it('should open the same page, intercept all xhr requests, and fail if any response is 403', () => {
    cy.visit('https://stage-app.ironwatchers.com/')

    cy.intercept('GET', '**').as('xhr')

    cy.wait('@xhr').then(({ response }) => {
      expect(response.statusCode).to.not.equal(403)
    })
  })
})

describe('Change Page Check Content Changed', () => {
  it('should visit the page, wait for all elements to load, save the content before and after clicking the element, and compare the content', () => {
    cy.visit('https://stage-app.ironwatchers.com/')

    let contentBeforeClick
    let contentAfterClick

    // Intercept GET requests
    cy.intercept('GET', '**').as('xhr')

    // Wait for the intercepted GET request
    cy.wait('@xhr').then(({ response }) => {
      contentBeforeClick = response.body
    })

    cy.get('#root > div > div > div:nth-child(3) > ul > li.ant-pagination-item.ant-pagination-item-2 > a').click()

    // Wait for all elements to load
    cy.wait('@xhr').then(({ response }) => {
      contentAfterClick = response.body

      // Compare the content before and after clicking the element
      expect(contentAfterClick).to.not.equal(contentBeforeClick)
    })
  })
})
