import React from "react";
import "./Login.css";

import {startPasswordlessRaw} from "./API";

import "bootstrap/dist/css/bootstrap.min.css";
import {
    FormGroup,
    FormLabel,
    FormControl,
    Button,
    Card,
    Modal
} from "react-bootstrap";

import ClipLoader from 'react-spinners/ClipLoader';

const Login: React.FC = () => {
    const [email, setEmail] = React.useState("");
    const [showModal, setShowModal] = React.useState(false);
    const [modalContent, setModalContent] = React.useState("");
    const [successfullSent, setSuccessfullSent] = React.useState(false);
    const [loading, setLoading] = React.useState(false);
    
    function handleSubmit(e: any) {
        e.preventDefault();
        let data = {
	        email: email,
	        redirectUri: window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + "/login/parser/"
        }
        
        setLoading(true);
        startPasswordlessRaw(data)
	        .then((response) => {
	            if (response.status !== 204) {
		            // Something went wrong on server side.
		            console.log(response);
		            if (response.status === 503) {
		                setModalContent("There was a problem with mail service. Please contact an admin about that.");
		            } else {
		                setModalContent("Something went wrong... Please try again later.");
		            }
		            setShowModal(true);
	            } else {
		            // Everything is good.
		            setSuccessfullSent(true);
	            }
                setLoading(false);
	        }).catch((error) => {
	            // Something went wrong with sending.
	            if (error.response.status === 429) {
		            setModalContent("You requested another verification code without using previous one. Please try again later.");
	            } else {
		            console.log(error);
		            setModalContent("Something went wrong... Please try again later.");
	            }
	            setShowModal(true);
                setLoading(false);
	        });
    }
    
    function validateForm() {
        return email.length > 0;
    }
    
    return (
        <div className="container-fluid">
            <div className="Login">
	            <Modal show={showModal} onHide={() => {setShowModal(false);}}>
	                <Modal.Header closeButton>
	                    <Modal.Title>Success</Modal.Title>
	                </Modal.Header>
	                <Modal.Body>{modalContent}</Modal.Body>
	            </Modal>
                <Card bg="light" id="centered-form">
                    <Card.Body hidden={successfullSent || loading}>
                        <form onSubmit={handleSubmit}>
                            <FormGroup controlId="email">
                                <FormLabel>Email</FormLabel>
                                <FormControl
                                    autoFocus
                                    type="email"
                                    value={email}
                                    onChange={(e: any) => setEmail(e.target.value)}
                                />
                            </FormGroup>
                            <Button block disabled={!validateForm()} type="submit">
                                Login
                            </Button>
                        </form>
                    </Card.Body>
	                <div>
	                    <Card.Body hidden={!successfullSent || loading}>
	                        <Card.Title>Good job!</Card.Title>
	                        If your mail is in our database, you will shortly get a message with an one-time authenticating link. Click it, and you will be logged in.
	                    </Card.Body>
	                    <Card.Body hidden={!loading}>
	                        <ClipLoader
	                            size={150}
	                        />
	                    </Card.Body>
	                </div>
                </Card>
            </div>
        </div>
    );
};

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
    setToken("");
}

export default Login;
