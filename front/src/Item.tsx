import React from "react";

import "bootstrap/dist/css/bootstrap.min.css";

//import axios from "axios";
//import ClipLoader from 'react-spinners/ClipLoader';

type ItemProps = {
    id : number;
    url : string;
    sleepTime : number;
    makeScreenshots : boolean;
}

type ItemState = {
}

class Item extends React.Component<ItemProps, ItemState> {
    state : ItemState = {}

    render () {
  return (
      <div className="Item">
	<a href={this.props.url}>{this.props.url}</a>|
	sleep time: {this.props.sleepTime} minutes|
	diff screenshots: {this.props.makeScreenshots.toString()}
      </div>
  );
    }
};

export default Item;
