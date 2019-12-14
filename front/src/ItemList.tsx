import React from "react";

import {Button} from "react-bootstrap";
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
			 <Item key={item.id} id={item.id} url={item.url} sleepTime={item.sleepTime} makeScreenshots={item.makeScreenshots} />)
    }
    
  return (
      <div className="ItemList">
	{renderItems(props.items)}
      </div>
  );
};

export default ItemList;
