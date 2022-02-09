// Read the API_URL from .env file during the development and from window._env_ in production

declare global {
    interface Window {
        _env_: {
            REACT_APP_API_URL: string,
            USE_ENV_REACT_APP_API_URL: string
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
    return 'api.' + window.location.hostname;
}

export const API_URL: string = getAPIURL();
