import React from "react";

import {Form, Button, Modal, ToggleButton, ToggleButtonGroup, ListGroup} from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

import Item from "./Item";
import ItemProps from "./Item";
//import axios from "axios";
//import ClipLoader from 'react-spinners/ClipLoader';

type ItemListProps = {
    items : Array<ItemProps["props"]>;
    visibleCount : number;
}

type EditModalProps = {show: boolean; onHide: any; item: ItemProps["props"] | null}

function EditModal (props : EditModalProps) {

    function content(item : ItemProps["props"] | null) {
	if (item == null) {
	    return (
		<Modal show={props.show} onHide={props.onHide}>
		  <Modal.Header closeButton>
		    <Modal.Title>Empty Modal</Modal.Title>
		  </Modal.Header>
		  <Modal.Body>
		    temp
		  </Modal.Body>
		</Modal>
	    )
	}
	else {
	    return (
		<Modal show={props.show} onHide={props.onHide}>
		  <Modal.Header closeButton>
		    <Modal.Title>Editing item {item.id}</Modal.Title>
		  </Modal.Header>
		  <Modal.Body>
		    <Form>
		      <Form.Group controlId="formBasicEmail">
			<Form.Label>Email address</Form.Label>
			<Form.Control type="email" placeholder="Enter email" />
			<Form.Text className="text-muted">
			</Form.Text>
		      </Form.Group>

		      <Form.Group controlId="formBasicPassword">
			<Form.Label>Password</Form.Label>
			<Form.Control type="password" placeholder="Password" />
		      </Form.Group>
		      <Form.Group controlId="formBasicCheckbox">
			<Form.Check type="checkbox" label="Check me out" />
		      </Form.Group>
		      <Button variant="primary" type="submit">
			Submit
		      </Button>
		    </Form>
		  </Modal.Body>
		</Modal>
	    )
	}
    }

    return (
	<div>{content(props.item)}</div>
    )
}

function ItemList (props : ItemListProps) {
    // It's used to describe which tab is currently chosen (only visibleCount of items is display simultaenously).
    const [tab, setTab] = React.useState(0);
    const [showEditModal, setShowEditModal] = React.useState(false);
    const [editModal, setEditModal] = React.useState("");
    const [activeItem, setActiveItem] = React.useState(null);

    function renderItems(items : Array<ItemProps["props"]>, visibleCount : number) {
	console.log(items);
	let offset = tab * visibleCount;
	return items.slice(offset, offset + visibleCount).map((item : ItemProps["props"], key) =>
							      <ListGroup.Item
							      onClick={(e : any) => itemClicked(item)}
							      key={item.id} action>
							      <Item
							      key={item.id}
							      id={item.id}
							      url={item.url}
							      sleepTime={item.sleepTime}
							      makeScreenshots={item.makeScreenshots} />
							      </ListGroup.Item>
							     )
    }

    function itemClicked(item : any) {
	console.log(item);
	setActiveItem(item);
	setShowEditModal(true);
    }

    function renderTabButtons(itemsCount : number, visibleCount : number) {
	let tabsCount = Math.ceil(itemsCount / visibleCount);
	let tabsIndexes = Array.from(Array(tabsCount).keys())
	return tabsIndexes.map((item) =>
			       <ToggleButton key={item} value={item}>{item}</ToggleButton>)
    }
    
  return (
      <div className="ItemList">
	<div className="Items m-2">
	  <ListGroup>
	    {renderItems(props.items, props.visibleCount)}
	  </ListGroup>
	</div>
	<div className="Controls m-2 mt-1">
	  <ToggleButtonGroup type="radio" onChange={(val : number) => setTab(val)} name="tab" defaultValue={0}>
	    {renderTabButtons(props.items.length, props.visibleCount)}
	  </ToggleButtonGroup>
	</div>
	<EditModal show={showEditModal} onHide={() => {setShowEditModal(false);}} item={activeItem}/>
      </div>
  );
};

export default ItemList;
