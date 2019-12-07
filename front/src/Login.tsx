import React from "react";
import "./Login.scss";

import "bootstrap/dist/css/bootstrap.min.css";
import {
  FormGroup,
  FormLabel,
  FormControl,
  Button,
  Card,
  Modal
} from "react-bootstrap";

import axios from "axios";
import ClipLoader from 'react-spinners/ClipLoader';

const Login: React.FC = () => {
  const [email, setEmail] = React.useState("");
  const [showModal, setShowModal] = React.useState(false);
  const [modalContent, setModalContent] = React.useState("");
  const [successfullSent, setSuccessfullSent] = React.useState(false);
  const [loading, setLoading] = React.useState(false);

  function handleSubmit(e: any) {
      e.preventDefault();
      let config = {timeout: 10000}
      let data = {
	  email: email,
	  redirectUri: window.location.protocol + "//" + window.location.hostname + "/login/parser/"
      }

      setLoading(true);
      axios.post(process.env.REACT_APP_API_SERVER + "/passwordless/start", data, config)
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
	  }).catch((error) => {
	    // Something went wrong with sending.
	      console.log(error);
	      setModalContent("Something went wrong... Please try again later.");
	      setShowModal(true);
	  });
      setLoading(false);
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
        // TODO: REMOVE IN PRODUCTION.
        if (process.env.NODE_ENV === "development") {
            window.sessionStorage.setItem(token_session_name, "DEV_TOKEN");
        }
       console.log(window.sessionStorage.getItem(token_session_name));
       return window.sessionStorage.getItem(token_session_name);
}

export function setToken(token : string) {
       window.sessionStorage.setItem(token_session_name, token);
}

export function logOut() {
       window.sessionStorage.setItem(token_session_name, "");
}

export default Login;
