// Read the API_URL from .env file during the development and from window._env_ in production

declare global {
    interface Window {
        _env_: { REACT_APP_API_URL: string };
    }
}

export const API_URL: string = process.env.NODE_ENV === "development" ? process.env.REACT_APP_API_URL as string : window._env_.REACT_APP_API_URL;
