import axios from "axios";

// It is used to get access token.
import {userMail, getToken} from "./Login";

// Ensuring that proper types are used.
import ItemProps from "./Item";



export function handleCreate(json : ItemProps["props"]) {
    console.log(json);
    console.log("REAL CREATE!");
    let config = {
	timeout : 10000,
        headers: {
            Authorization: "Bearer " + getToken()
        }
    }
    let data : ItemProps["props"] & {owner: string} = { ...json, ...{owner: userMail()}}

    axios.post(process.env.REACT_APP_API_SERVER + "/v1/item/create", data, config)
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

export function handleDelete(json : ItemProps["props"]) {
    console.log(json);
    console.log("REAL DELETE!");

    let config = {
	timeout : 10000,
        headers: {
            Authorization: "Bearer " + getToken()
        }
    }

    axios.delete(process.env.REACT_APP_API_SERVER + "/v1/item/delete/" + json.id, config)
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

export function handleUpdate(json : ItemProps["props"]) {
    console.log(json);
    console.log("REAL UPDATE!");
    let config = {
	timeout : 10000,
        headers: {
            Authorization: "Bearer " + getToken()
        }
    }
    let data : ItemProps["props"] & {owner: string} = { ...json, ...{owner: userMail()}}

    axios.put(process.env.REACT_APP_API_SERVER + "/v1/item/update/" + json.id, data, config)
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
