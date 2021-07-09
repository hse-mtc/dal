import jwtDecode from "jwt-decode";

class TokenService {
  get access() {
    return localStorage.getItem("access_token");
  }

  get refresh() {
    return localStorage.getItem("refresh_token");
  }

  get userId() {
    try {
      return jwtDecode(this.access).user_id;
    } catch {
      return null;
    }
  }

  /**
   *
   * @param { {access: string, refresh: string} } tokensObj - объект с токенами
   * @param { string } tokensObj.access - access токен
   * @param { string } tokensObj.refresh - refresh токен
   */
  setTokens({ access, refresh }) {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
  }

  clearTokens() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  }
}

export const tokenService = new TokenService();
