import history from './history';
import {isDev} from './Base';

const token_session_name = "auth_token";

export function getToken() {
    if (isDev()) {
        let devToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUudXJsIiwibmFtZSI6InRlc3R1c2VyIiwiaWF0IjoxNTE2MjM5MDIyfQ.FqZJO19KHW7EQoAf8LIVRu31nruBFLm4LrUBBSs_TQE'
        if (window.sessionStorage.getItem(token_session_name) == null) {
            return devToken;
        }
    }
    return window.sessionStorage.getItem(token_session_name);
}

export function setToken(token : string) {
    window.sessionStorage.setItem(token_session_name, token);
}

export function userId() {
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
