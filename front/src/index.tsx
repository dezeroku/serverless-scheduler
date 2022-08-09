import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Switch, Route, Redirect } from 'react-router-dom';
import './index.css';
import {getToken, setToken} from './Login';
import {loginURL, logoutURL} from "./Config";
import Home from './Home';
import * as serviceWorker from './serviceWorker';
import queryString from "query-string";
import history from './history';

ReactDOM.render((
    <Router history={history}>
        <Switch>
	        <Route path="/login/cognito-parser" component={LoginParser}>
	        </Route>
            <Route path='/login' component={() => {
                       // Just redirect to Cognito
                       window.location.href = loginURL;
                       return null;
                   }}/>
            <Route path='/logout-internal' component={() => {
                       // Go to Cognito to invalidate the session
                       window.location.href = logoutURL;
                       return null;
                   }}/>
            <Route path='/logout' component={() => {
                       // We came here from Cognito
                       setToken('');
                       history.push('/');
                       return null;
                   }}/>
	        <PrivateRoute path="/">
	            <Home />
	        </PrivateRoute>
        </Switch>
    </Router>), document.getElementById('root'));

function LoginParser(props : any) {
    // TODO: also properly handle the access time, what to do when it expires?
    let responseData = queryString.parse(props.location.hash);
    if (typeof responseData.access_token === "string") {
        setToken(responseData.access_token as string);
    } else {
        alert('Seems that this page was accessed without a token!');
    }
    return <Redirect to="/" />;
}

function PrivateRoute({ children, ...rest } : any) {
    return (
        <Route
            {...rest}
            render={({ location }) =>
                getToken() ? (
                    children
                ) : (
                    <Redirect
                        to={{
                            pathname: "/login",
                            state: { from: location }
                        }}
                    />
                )
            }
        />
    );
}

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
