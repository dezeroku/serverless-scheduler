import axios from "axios";

// It is used to get access token.
import {userMail, getToken} from "./Login";
import {API_URL} from "./Config";

// Ensuring that proper types are used.
import ItemProps from "./Item";

type PasswordlessRawData = {
    email: string;
    redirectUri: string;
}

export async function startPasswordlessRaw(data: PasswordlessRawData) {
    let config = {timeout: 10000}
    return axios.post(API_URL + "/passwordless/start", data, config)
}

export async function getItemsRaw() {
	let config = {
        headers: {
            Authorization: "Bearer " + getToken()
        }
    }

    return axios.get(API_URL + "/v1/items/" + userMail(), config)
}

export async function handleCreate(json : ItemProps["props"]) {
    console.log(json);
    console.log("REAL CREATE!");
    let config = {
	    timeout : 10000,
        headers: {
            Authorization: "Bearer " + getToken()
        }
    }
    let data : any = { ...json, ...{owner: userMail()}}
    data["sleepTime"] *= 60;
    
    return axios.post(API_URL + "/v1/item/create", data, config)
	    .then((response) => {
	        console.log("AA");
	        if (response.status !== 200) {
		        // Something went wrong on server side.
		        console.log(response);
		        return "Something went wrong... Please try again later."
	        } else {
		        return "Successfully updated!"
		        // Everything is good.
	        }
	    }).catch((error) => {
	        // Something went wrong with sending.
	        console.log(error.response);
	        if (error.response.status === 401) {
		        return "You are unauthorized!"
	        } else if (error.response.status === 400 || error.response.status === 422) {
		        return "Incorrect input data, please contact administrator"
	        } else {
		        return "Something went wrong... Please try again later."
	        }
	    });
}

export async function handleDelete(json : ItemProps["props"]) {
    console.log(json);
    console.log("REAL DELETE!");
    
    let config = {
	    timeout : 10000,
        headers: {
            Authorization: "Bearer " + getToken()
        }
    }
    
    return axios.delete(API_URL + "/v1/item/delete/" + json.id, config)
	    .then((response) => {
	        console.log("AA");
	        if (response.status !== 200) {
		        // Something went wrong on server side.
		        console.log(response);
		        return "Something went wrong... Please try again later."
	        } else {
		        return "Successfully updated!"
		        // Everything is good.
	        }
	    }).catch((error) => {
	        // Something went wrong with sending.
	        console.log(error.response);
	        if (error.response.status === 401) {
		        return "You are unauthorized!"
	        } else if (error.response.status === 400 || error.response.status === 422) {
		        return "Incorrect input data, please contact administrator"
	        } else {
		        return "Something went wrong... Please try again later."
	        }
	    });
}

export async function handleUpdate(json : ItemProps["props"]) {
    console.log(json);
    console.log("REAL UPDATE!");
    let config = {
	    timeout : 10000,
        headers: {
            Authorization: "Bearer " + getToken()
        }
    }
    let data : any = { ...json, ...{owner: userMail()}}
    data["sleepTime"] *= 60;
    
    return axios.put(API_URL + "/v1/item/update/" + json.id, data, config)
	    .then((response) => {
	        console.log("AA");
	        if (response.status !== 200) {
		        // Something went wrong on server side.
		        console.log(response);
		        return "Something went wrong... Please try again later."
	        } else {
		        return "Successfully updated!"
		        // Everything is good.
	        }
	    }).catch((error) => {
	        // Something went wrong with sending.
	        console.log(error.response);
	        if (error.response.status === 401) {
		        return "You are unauthorized!"
	        } else if (error.response.status === 400  || error.response.status === 422) {
		        return "Incorrect input data, please contact administrator"
	        } else {
		        return "Something went wrong... Please try again later."
	        }
	    });
}
