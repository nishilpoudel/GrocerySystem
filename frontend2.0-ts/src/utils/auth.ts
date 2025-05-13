// Some utility file that gets and sets the token for usage later

let accessToken: string | null;

export function setAccessToken(token: string) {
  accessToken = token;
}

export function getAccessToken(): string | null {
  return accessToken;
}
