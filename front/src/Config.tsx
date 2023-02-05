// Read the API_URL from .env file during the development and from window._env_ in production

declare global {
    interface Window {
        _env_: {
            REACT_APP_API_URL: string,
            USE_ENV_REACT_APP_API_URL: string,
            USE_ENV_LOGIN_REDIRECT: string,
            USE_ENV_FRONT_DOMAIN: string,
            CLIENT_POOL_ID: string,
            FRONT_DOMAIN: string
        };
    }
}

function getAPIURL() : string {
    if (process.env.NODE_ENV === "development") {
        return process.env.REACT_APP_API_URL as string;
    } else {
        if (window._env_.USE_ENV_REACT_APP_API_URL === 'true') {
            return window._env_.REACT_APP_API_URL;
        }
    }
    // Try to automagically generate it based on the domain
    return 'https://api.' + window.location.hostname;
}

function getFrontDomain() : string {
    if (process.env.NODE_ENV === "development") {
        if (process.env.USE_ENV_FRONT_DOMAIN === "true") {
            return process.env.FRONT_DOMAIN as string;
        }
    } else {
        if (window._env_.USE_ENV_FRONT_DOMAIN === "true") {
            return window._env_.FRONT_DOMAIN;
        }
    }

    return window.location.hostname;
}

function getUseEnvLoginRedirect() : string {
    if (process.env.NODE_ENV === "development") {
        return process.env.USE_ENV_LOGIN_REDIRECT as string;
    } else {
        return window._env_.USE_ENV_LOGIN_REDIRECT;
    }
}

function getClientPoolId() : string {
    if (process.env.NODE_ENV === "development") {
        return process.env.CLIENT_POOL_ID as string;
    } else {
        return window._env_.CLIENT_POOL_ID;
    }
}

function getAuthorizeURL() : string {

    if (getUseEnvLoginRedirect() === "true") {
        let frontDomain = getFrontDomain();
        let clientPoolID = getClientPoolId();
        return "https://"
            + "auth."
            + frontDomain
            + "/oauth2/authorize?client_id="
            + clientPoolID
            + "&response_type=code&scope="
            + "email+openid+profile&redirect_uri="
            + "https://"
            + frontDomain
            + "/login/cognito-parser"
    }

    // Fallback to lambda intermediate endpoint
    return API_URL + "/v1/login/cognito-login";
}


function getTokenURL(code: string) : string {

    //if (getUseEnvLoginRedirect() === "true") {
        let frontDomain = getFrontDomain();
        let clientPoolID = getClientPoolId();
        return "https://"
            + "auth."
            + frontDomain
            + "/oauth2/token?client_id="
            + clientPoolID
            + "&grant_type=authorization_code"
            + "&redirect_uri="
            + "https://"
            + frontDomain
            + "/login/cognito-parser"
            + "&code=" + code
    //}

    // Fallback to lambda intermediate endpoint
    //return API_URL + "/v1/login/cognito-login";
}


function getLogoutURL() : string {
    if (getUseEnvLoginRedirect() === "true") {
        let frontDomain = getFrontDomain();
        let clientPoolID = getClientPoolId();

        return "https://"
            + "auth."
            + frontDomain
            + "/logout?client_id="
            + clientPoolID
            + "&logout_uri="
            + "https://"
            + frontDomain
            + "/logout"
    }

    // Fallback to lambda intermediate endpoint
    return API_URL + "/v1/login/cognito-logout";
}

export {getTokenURL};
export const API_URL: string = getAPIURL();

export const authorizeURL: string = getAuthorizeURL();
export const logoutURL: string = getLogoutURL();
