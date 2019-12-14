import React from "react";
//import "./Login.scss";

import {Route, Redirect} from "react-router-dom";
import {Button} from "react-bootstrap";
import {logOut, userMail, getToken} from "./Login";
import "bootstrap/dist/css/bootstrap.min.css";

import axios from "axios";
import ClipLoader from 'react-spinners/ClipLoader';

import ItemProps from './Item';
import ItemList from './ItemList';

type HomeProps = {
}

type HomeState = {
    loggedOut: boolean;
    loading: boolean;
    items: Array<ItemProps["props"]>;
}

class Home extends React.Component<HomeProps, HomeState> {
    state: HomeState = {
        loggedOut: false,
        loading: false,
	items: Array(0).fill(null)
    }

    componentDidMount() {
	this.setState({loading: true});
        console.log(userMail());
        let config = {
            headers: {
                Authorization: "Bearer " + getToken()
            }
        }

	axios.get(process.env.REACT_APP_API_SERVER + "/v1/items/" + userMail(), config)
	    .then((response) => {
		console.log(response.data);
                this.setState({loading: false});
	      if (response.status !== 200) {
                  // Something went wrong on server side.
		  console.log(response);
	      } else {
		  this.setState({items: response.data});
		  // Everything is good.
	      }
            }).catch((error) => {
                console.log(error);
                if (error.response.status === 401) {
                    alert("Your session timed out!");
		    this.handleLogout();
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
        {this.state.loading ? <ClipLoader size={150} /> : <ItemList items={this.state.items}/>}
	MAIN PAGE!!!
	<Route exact path="/">
	  {this.state.loggedOut ? <Redirect to="/login" /> : <div></div>}
	</Route>
      </div>
  );
    }
};

export default Home;
