import React from "react";
//import "./Login.scss";

import {Route, Redirect} from "react-router-dom";
import {Button, Navbar, Nav, Form} from "react-bootstrap";
import {logOut, userMail, getToken} from "./Login";
import {handleUpdate, handleCreate, handleDelete} from "./API";

import "bootstrap/dist/css/bootstrap.min.css";

import axios from "axios";
import ClipLoader from 'react-spinners/ClipLoader';

import ItemProps from './Item';
import ItemList from './ItemList';
import EditModal from './EditModal';

type HomeProps = {
}

type HomeState = {
    loggedOut: boolean;
    loading: boolean;
    items: Array<ItemProps["props"]>;
    showCreateModal : boolean;
}

class Home extends React.Component<HomeProps, HomeState> {
    state: HomeState = {
        loggedOut: false,
        loading: true,
	items: Array(0).fill(null),
	showCreateModal : false
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
	      if (response.status !== 200) {
                  // Something went wrong on server side.
		  console.log(response);
	      } else {
		this.setState({items: response.data});
		  // Everything is good.
	      }
               this.setState({loading: false});
            }).catch((error) => {
                console.log(error);
		// Something went wrong with sending.
		this.setState({loading: false});

                if (error.response.status === 401) {
                    //alert("Your session timed out!");
		    this.handleLogout();
                }
	  });
    }

    handleLogout() {
    	logOut();
	this.setState({loggedOut: true});
    }

    openCreateModal() {
	this.setState({showCreateModal: true});
    }

    closeCreateModal() {
	this.setState({showCreateModal: false});
    }

    render () {
  return (
      <div className="container-fluid">
	<Navbar className="bg-light">
	  <Navbar.Brand>Page Monitor</Navbar.Brand>
	  <Navbar.Toggle aria-controls="basic-navbar-nav" />
	  <Navbar.Collapse id="basic-navbar-nav">
	    <Nav className="mr-auto">
	    </Nav>
	    <Form inline>
	      <Button variant="success" onClick={() => this.openCreateModal()} className="mr-2">Create</Button>
	      <Button variant="outline-primary" onClick={() => this.handleLogout()}>Log Out</Button>
	    </Form>
	  </Navbar.Collapse>
	</Navbar>
        {this.state.loading ? <ClipLoader size={150} /> : <ItemList items={this.state.items} visibleCount={5} handleUpdate={handleUpdate} handleDelete={handleDelete}/>}
	  <EditModal show={this.state.showCreateModal} handleTask={handleCreate} onHide={() => this.setState({showCreateModal: false})} item={null} editMode={false} handleDelete={handleDelete}/>

	<Route exact path="/">
	  {this.state.loggedOut ? <Redirect to="/login" /> : <div></div>}
	</Route>
      </div>
  );
    }
};

export default Home;