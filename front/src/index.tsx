import React from "react";
import ReactDOM from "react-dom";
import { Router, Switch, Route, Redirect } from "react-router-dom";
import "./index.css";
import { getToken, setToken } from "./Login";
import { authorizeURL, logoutURL, getTokenURL } from "./Config";
import Home from "./Home";
import * as serviceWorker from "./serviceWorker";
import queryString from "query-string";
import history from "./history";

ReactDOM.render(
  <Router history={history}>
    <Switch>
      <Route path="/login/cognito-parser" component={LoginParser}></Route>
      <Route
        path="/login"
        component={() => {
          // Just redirect to Cognito
          window.location.href = authorizeURL;
          return null;
        }}
      />
      <Route
        path="/logout-internal"
        component={() => {
          // Go to Cognito to invalidate the session
          window.location.href = logoutURL;
          return null;
        }}
      />
      <Route
        path="/logout"
        component={() => {
          // We came here from Cognito
          setToken("");
          history.push("/");
          return null;
        }}
      />
      <PrivateRoute path="/">
        <Home />
      </PrivateRoute>
    </Switch>
  </Router>,
  document.getElementById("root")
);

function LoginParser(props: any) {
  // TODO: also properly handle the access time, what to do when it expires?
  let responseData = queryString.parse(props.location.search);
  console.log(responseData);
  if (typeof responseData.code === "string") {
    // This is an authorization code, now let's obtain the real token
    let code = responseData.code;

    // This is synchronous and ugly
    // Oh well, it all needs a rewrite anyway
    const request = new XMLHttpRequest();
    request.open("POST", getTokenURL(code), false);
    request.setRequestHeader(
      "Content-Type",
      "application/x-www-form-urlencoded"
    );
    request.send(null);

    if (request.status !== 200) {
      alert("Something went wrong!");
    } else {
      const parsed = JSON.parse(request.response);
      setToken(parsed.id_token as string);
    }
  } else {
    alert("Seems that this page was accessed without an auth code!");
  }
  return <Redirect to="/" />;
}

function PrivateRoute({ children, ...rest }: any) {
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
              state: { from: location },
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
