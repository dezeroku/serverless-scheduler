import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Switch, Route, Redirect } from 'react-router-dom';
import './index.css';
import Login, {getToken, setToken} from './Login';
import * as serviceWorker from './serviceWorker';
import queryString from "query-string";

ReactDOM.render((
    <Router>
      <Switch>
	    <Route path="/login/parser" component={LoginParser}>
	    </Route>
            <Route path="/login">
              <Login />
            </Route>
	    <PrivateRoute path="/">
	      <Home />
	    </PrivateRoute>
        </Switch>
    </Router>), document.getElementById('root'));

function LoginParser(props : any) {
    let responseData = queryString.parse(props.location.hash);
    if (typeof responseData.jwt === "string") {
       setToken(responseData.jwt);
    }
    return <Redirect to="/" />;
}

function Home() {
    return <h2>Home</h2>;
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
