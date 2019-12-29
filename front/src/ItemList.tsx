import React from "react";

import {Button, ListGroup} from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

import Item from "./Item";
import ItemProps from "./Item";
//import axios from "axios";
//import ClipLoader from 'react-spinners/ClipLoader';

type ItemListProps = {
    items : Array<ItemProps["props"]>;
}

function ItemList (props : ItemListProps) {

    function renderItems(items : Array<ItemProps["props"]>) {
	console.log(items);
	return items.map((item : ItemProps["props"], key) =>
			 <ListGroup.Item key={item.id} action><Item key={item.id} id={item.id} url={item.url} sleepTime={item.sleepTime} makeScreenshots={item.makeScreenshots} /></ListGroup.Item>)
    }
    
  return (
      <div className="ItemList">
	<ListGroup>
	{renderItems(props.items)}
	</ListGroup>
      </div>
  );
};

export default ItemList;
