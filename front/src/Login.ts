import history from './history';

const token_session_name = "auth_token";

export function getToken() {
    return window.sessionStorage.getItem(token_session_name);
}

export function setToken(token : string) {
    window.sessionStorage.setItem(token_session_name, token);
}

export function userMail() {
    let token = getToken();
    
    if (token !== null) {
        let parsed = parseJwt(token);
        // TODO: add check for expiration date
        if (parsed !== null) {
            if ("sub" in parsed) {
                return parsed.sub;
            }
        }
    }
    
    return null;
}

export function parseJwt (token : string) {
    try {
        return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
        return null;
    }
};

export function logOut() {
    // The /logout endpoint (that we'll be redirected to from Cognito) will take care of resetting token
    // TODO: Is this correct approach? Doesn't seem really mockable.
    history.push('/logout-internal');
    return null;
}
