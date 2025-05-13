import { setAccessToken, getAccessToken } from "../utils/auth";

interface RefreshResponse {
  access_token: string;
  token_type: string;
}

export async function fetchWithAuth(
  input: RequestInfo,
  init: RequestInit = {}
): Promise<Response> {
  const headers = new Headers(init.headers || undefined);

  const token = getAccessToken();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const opts: RequestInit = {
    ...init,
    headers,
    credentials: "include",
  };

  let response = await fetch(input, opts);

  if (response.status === 401) {
    // if the response status is 401(unauthorized ), then we hit the refresh endpoint
    const refreshRes = await fetch("http://localhost:8000/refresh", {
      method: "POST",
      credentials: "include",
    });

    if (refreshRes.ok) {
      const data = (await response.json()) as RefreshResponse;
      setAccessToken(data.access_token);

      // now we can retry the original request
      headers.set("Authorization", `Bearer ${data.access_token}`);
      response = await fetch(input, { ...opts, headers });
    } else {
      throw new Error("Session Expired : Please log in again ");
    }
  }
  return response;
}
