import {handleLogout} from "./API";

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
    handleLogout().then((response) => {
	    if (response.status !== 200) {
            alert('Could not log out, try again');
		    console.log(response);
	    } else {
            setToken("");
	    }
    }).catch((error) => {
        console.log(error);
        alert('Could not request logout, try again');
	});

    return null;
}
