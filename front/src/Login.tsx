import React from "react";
import "./Login.scss";

import "bootstrap/dist/css/bootstrap.min.css";
import {
  FormGroup,
  FormLabel,
  FormControl,
  Button,
  Card
} from "react-bootstrap";

const Login: React.FC = () => {
  const [email, setEmail] = React.useState("");

  function handleSubmit(e: any) {
    e.preventDefault();
    console.log("SUBMIT!");
  }

  function validateForm() {
    return email.length > 0;
  }

  return (
    <div className="container-fluid">
      <div className="Login">
        <Card bg="light" id="centered-form">
          <Card.Body>
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
        </Card>
      </div>
    </div>
  );
};

export default Login;
