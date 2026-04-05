import { sha1, callMailgunApi } from "./utils";

// Environment variables used in the handler:
//   MAILGUN_API_KEY      - Mailgun private API key
//   MAILGUN_MAILING_LIST - Mailgun mailing list email address, e.g. news@mydomain.com
//   CONFIRM_SECRET       - A random value that is used to calculate email confirmation code

// Function GET handler
export async function onRequestGet(context) {
  const { request, env } = context;

  // get request params
  const { searchParams } = new URL(request.url)
  const email = searchParams.get('email')
  const code = searchParams.get('code')

  if (!code || !email) {
    throw "Invalid request parameters"
  }

  // validate confirmation code
  const calculatedCode = await sha1(email + env.CONFIRM_SECRET)
  if (calculatedCode !== code) {
    throw "Invalid email or confirmation code"
  }

  // update subscription status
  await subscribeMailingListMember(env.MAILGUN_API_KEY, env.MAILGUN_MAILING_LIST, email);

  // redirect to a home page
  return Response.redirect(new URL(request.url).origin + "?signup-confirmed", 302)
}

// Updates mailing list member's status to "subscribed=yes"
async function subscribeMailingListMember(mailgunApiKey, listName, memberAddress) {
  const data = {
    address: memberAddress,
    subscribed: 'yes'
  }

  const response = await callMailgunApi(mailgunApiKey,
    'PUT', `https://api.mailgun.net/v3/lists/${listName}/members/${encodeURIComponent(memberAddress)}`, data)

  if (response.status === 200) {
    return true; // member has been subscribed
  } else {
    const responseBody = await response.text()
    throw `Error updating mailing list member: ${responseBody}`
  }
}