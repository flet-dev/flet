import { urlEncodeObject, sha1, callMailgunApi } from "./utils";
import { fromTemplate, subjectTemplate, bodyTemplate } from "./email-template"

// Environment variables used in the handler:
//   HCAPTCHA_SECRET      - A secret corresponding to a site key and used to verify your hCaptcha account
//   MAILGUN_API_KEY      - Mailgun private API key
//   MAILGUN_MAILING_LIST - Mailgun mailing list email address, e.g. news@mydomain.com
//   CONFIRM_SECRET       - A random value that is used to calculate email confirmation code

// Function POST handler
export async function onRequestPost(context) {
  const { request, env } = context;
  const { headers } = request;

  // validate content type
  const contentType = headers.get('content-type');
  if (!contentType.includes('application/json')) {
    throw "Content type not recognized"
  }

  // get request body
  const reqBody = await request.json();
  const email = reqBody.email;
  const captchaToken = reqBody.captchaToken;

  // verify parameters
  if (!email || !captchaToken) {
    throw "Invalid request parameters"
  }

  // validate hCaptcha response
  await validateCaptcha(captchaToken, env.HCAPTCHA_SECRET)

  // add email address to the mailing list
  var added = await addMailingListMember(env.MAILGUN_API_KEY, env.MAILGUN_MAILING_LIST, email);
  if (added) {
    // build confirmation link
    const urlParams = {
      email: email,
      code: await sha1(email + env.CONFIRM_SECRET)
    }
    const url = new URL(request.url);

    var templateData = {
      confirmUrl: `${url.origin}/api/confirm-subscription?${urlEncodeObject(urlParams)}`
    }

    // send email with a confirmation link
    await sendEmail(env.MAILGUN_API_KEY, env.MAILGUN_MAILING_LIST.split('@').pop(),
      fromTemplate(templateData), email, subjectTemplate(templateData), bodyTemplate(templateData));
  }

  // send successful response
  return new Response(JSON.stringify({ result: "OK" }), {
    headers: { 'content-type': 'application/json' }
  })
}

// Validates hCaptcha response and throws if invalid
async function validateCaptcha(token, secret) {
  const data = {
    response: token,
    secret: secret
  }

  const encData = urlEncodeObject(data)
  const captchaResponse = await fetch(
    `https://hcaptcha.com/siteverify`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': encData.length.toString()
      },
      body: encData
    }
  )
  const captchaBody = await captchaResponse.json()
  if (!captchaBody.success) {
    throw captchaBody["error-codes"]
  }
}

// Adds a new member (email address) into Mailgun mailing list
// returns `true` if the member was successfully added
// returns `false` if the member already exists in the list
async function addMailingListMember(mailgunApiKey, listName, memberAddress) {
  const data = {
    address: memberAddress,
    subscribed: 'no',
    upsert: 'no'
  }

  const response = await callMailgunApi(mailgunApiKey,
    'POST', `https://api.mailgun.net/v3/lists/${listName}/members`, data)

  if (response.status === 200) {
    return true; // member has been added
  } else if (response.status === 400) {
    return false; // member already added
  } else {
    const responseBody = await response.json()
    throw `Error adding mailing list member: ${responseBody.message}`
  }
}

// Sends email message via Mailgun API
async function sendEmail(mailgunApiKey, mailDomain, from, to, subject, htmlBody) {
  const data = {
    from: from,
    to: to,
    subject: subject,
    html: htmlBody
  }

  const response = await callMailgunApi(mailgunApiKey,
    'POST', `https://api.mailgun.net/v3/${mailDomain}/messages`, data)

  if (response.status !== 200) {
    const responseBody = await response.text()
    throw `Error sending email message: ${responseBody}`
  }
}
