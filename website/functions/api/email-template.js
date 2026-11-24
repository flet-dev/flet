export function fromTemplate(data) {
  return `Flet <hello@flet.dev>`
}

export function subjectTemplate(data) {
  return `Confirm your subscription to Flet mailing list`
}

export function bodyTemplate(data) {
  return `
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Email Template</title>
        <link
          rel="stylesheet"
          href="https://unpkg.com/modern-css-reset/dist/reset.min.css"
        />
      </head>
      <body>
        <p>
            <a href="${data.confirmUrl}">Click here to confirm</a> your subscription to Flet project mailing list!
        </p>
        <p>
            If you didn't subscribe to this list or you're not sure why you received this email, you can delete it. You will not be subscribed if you don't click on the link above.
        </p>
      </body>
    </html>
  `
}