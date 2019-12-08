import React from "react";
//import "./Login.scss";

import {Route, Redirect} from "react-router-dom";
import {Button} from "react-bootstrap";
import {logOut, userMail, getToken} from "./Login";
import "bootstrap/dist/css/bootstrap.min.css";

import axios from "axios";
import ClipLoader from 'react-spinners/ClipLoader';

type HomeState = {
    loggedOut: boolean;
}

class Home extends React.Component<HomeState> {
    state: HomeState = {
	loggedOut: false
    }

    componentDidMount() {
        console.log(userMail());
        let config = {
            headers: {
                Authorization: "Bearer " + getToken()
            }
        }

	this.setState({loading: true});
	axios.get(process.env.REACT_APP_API_SERVER + "/v1/items/" + userMail(), config)
	    .then((response) => {
                this.setState({loading: false});
	      if (response.status !== 200) {
                  // Something went wrong on server side.
		  console.log(response);
	      } else {
		  // Everything is good.
	      }
            }).catch((error) => {
                console.log(error);
                if (error.response.status === 401) {
                    alert("Your session timed out!");
                    logOut();
                    this.forceUpdate();
                }
	    // Something went wrong with sending.
	      this.setState({loading: false});
	      console.log(error);
	  });
    }

    handleLogout() {
    	logOut();
	this.setState({loggedOut: true});
    }

    render () {
  return (
      <div className="container-fluid">
	<Button onClick={() => {this.handleLogout();}}>Log Out</Button>
	<ClipLoader
	  size={150}
	  />
	MAIN PAGE!!!
	<Route exact path="/">
	  {this.state.loggedOut ? <Redirect to="/login" /> : <div></div>}
	</Route>
      </div>
  );
    }
};

export default Home;
