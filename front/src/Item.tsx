import React from "react";

import {Button} from "react-bootstrap";
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

    constructor(props : ItemProps) {
	super(props);
    }

    render () {
  return (
      <div className="Item">
	{this.props.id}|{this.props.url}|{this.props.sleepTime}|{this.props.makeScreenshots.toString()}
      </div>
  );
    }
};

export default Item;
