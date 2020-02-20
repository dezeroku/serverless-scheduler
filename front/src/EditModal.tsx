import React from "react";

import "bootstrap/dist/css/bootstrap.min.css";
import {
  Form,
  Button,
  Modal
} from "react-bootstrap";
import ClipLoader from 'react-spinners/ClipLoader';

import ItemProps from "./Item";


type EditModalProps = {show: boolean; onHide: any; item: ItemProps["props"] | null; handleTask: any; handleDelete: any; editMode: boolean}

function EditModal (props : EditModalProps) {

    const [loading, setLoading] = React.useState(false);

    const handleTaskLocal = (event : any) => {
	// Get data to json form and send it to higher level handler.
	const form = event.currentTarget;
	event.preventDefault();
	event.stopPropagation();

	let json : ItemProps["props"] = {
	    id: parseInt(form.id.value),
	    url: form.url.value,
	    sleepTime: parseInt(form.sleepTime.value),
	    makeScreenshots: form.makeScreenshots.checked,
	}

	setLoading(true);
	let result : string = props.handleTask(json);
	setLoading(false);
	//alert(result);
	window.location.reload();
    }

    function handleDeleteLocal(id : number) {
	// Get data to json form and send it to higher level handler.

	let json : ItemProps["props"] = {
	    id: id,
	    url: "",
	    sleepTime: 0,
	    makeScreenshots: false,
	}

	setLoading(true);
	let result : string = props.handleDelete(json);
	setLoading(false);
	//alert(result);
	window.location.reload();
    }

    
    function content(item : ItemProps["props"] | null) {
	// If item is provided (update scenario) use data from it.
	// If not (create scenario), create an example object.
	var temp : ItemProps["props"]
	if (item == null) {
	    temp = {
		id: 0,
		url: "",
		sleepTime: 60,
		makeScreenshots: true}
	} else {
	    temp = item
	}

	return (
	    <Modal show={props.show} onHide={props.onHide}>
	      <Modal.Header closeButton>
		<Modal.Title>Editing monitor job of {temp.url}</Modal.Title>
	      </Modal.Header>
	      <Modal.Body hidden={loading}>
		<Form onSubmit={handleTaskLocal}>
		  <Form.Group controlId="id">
		    <Form.Control type="hidden" value={temp.id.toString()}/>
		  </Form.Group>
		  <Form.Group controlId="url">
		    <Form.Label>URL of the page you want to monitor</Form.Label>
		    <Form.Control type="url" defaultValue={temp.url}/>
		    <Form.Text className="text-muted">
		    </Form.Text>
		  </Form.Group>
		  <Form.Group controlId="sleepTime">
		    <Form.Label>How often (in minutes) should the page be checked</Form.Label>
		    <Form.Control as="select">
		      <option>{temp.sleepTime}</option>
		      <option>2</option>
		      <option>5</option>
		      <option>10</option>
		      <option>15</option>
		      <option>20</option>
		      <option>30</option>
		      <option>60</option>
		      <option>120</option>
		      <option>300</option>
		      <option>720</option>
		      <option>1440</option>
		    </Form.Control>
		  </Form.Group>
		  <Form.Group controlId="makeScreenshots">
		    <Form.Check type="checkbox" label="Make screenshots" defaultChecked={temp.makeScreenshots}/>
		    <Form.Label>When checked, screenshots of changes will be attached to notification</Form.Label>
		  </Form.Group>
		  <Button variant="primary" type="submit">
		    {props.editMode ? "Update" : "Create"}
		  </Button>
		  {
		      props.editMode ? 
			  <Button type="button" variant="danger" onClick={() => handleDeleteLocal(temp.id)} className="float-right">Delete</Button> :
			      <div></div>
			  }
		</Form>
	      </Modal.Body>
	      <Modal.Body hidden={!loading}>
		<ClipLoader
		  size={150}
		  />
	      </Modal.Body>
	    </Modal>
	)
    }

    return (
	<div>{content(props.item)}</div>
    )
}

export default EditModal;
