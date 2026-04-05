export function urlEncodeObject(obj) {
    return Object.keys(obj)
      .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(obj[k]))
      .join('&')
  }

export async function sha1(str) {
    var buffer = await crypto.subtle.digest("SHA-1", new TextEncoder("utf-8").encode(str));
    return Array.prototype.map.call(new Uint8Array(buffer), x=>(('00'+x.toString(16)).slice(-2))).join('');
}

export function callMailgunApi(mailgunApiKey, method, url, data) {
    const encData = urlEncodeObject(data)
    return fetch(
      url,
      {
        method: method,
        headers: {
          Authorization: 'Basic ' + btoa('api:' + mailgunApiKey),
          'Content-Type': 'application/x-www-form-urlencoded',
          'Content-Length': encData.length.toString()
        },
        body: encData
      }
    )
  }