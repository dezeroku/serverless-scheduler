import React from "react";

import "bootstrap/dist/css/bootstrap.min.css";
import {
    Form,
    Button,
    Modal
} from "react-bootstrap";
import ClipLoader from 'react-spinners/ClipLoader';

import ItemProps from "./Item";


type EditModalProps = {show: boolean; onHide: any; item: ItemProps["props"] | null; handleTask: any; handleDelete: any; editMode: boolean; closeModal: any; refresh: any}

function EditModal (props : EditModalProps) {

    const [loading, setLoading] = React.useState(false);

    const handleTaskLocal = async (event : any) => {
	    // Get data to json form and send it to higher level handler.
	    const form = event.currentTarget;
	    event.preventDefault();
	    event.stopPropagation();

	    let json : ItemProps["props"] = {
	        job_id: parseInt(form.id.value),
	        url: form.url.value,
	        sleep_time: parseInt(form.sleep_time.value),
	        make_screenshots: form.make_screenshots.checked,
	    }

	    setLoading(true);
	    let result : string = await props.handleTask(json);
	    setLoading(false);
	    props.closeModal()
	    props.refresh()
        //alert(props.editMode ? "Updated" : "Created");
        //window.location.reload();
    }

    const handleDeleteLocal = async (id : number) => {
	    // Get data to json form and send it to higher level handler.

	    let json : ItemProps["props"] = {
	        job_id: id,
	        url: "",
	        sleep_time: 0,
	        make_screenshots: false,
	    }

	    setLoading(true);
	    let result : string = await props.handleDelete(json);
	    setLoading(false);
	    props.closeModal()
	    props.refresh()
        //alert(result);
        //window.location.reload();
    }


    function content(item : ItemProps["props"] | null) {
	    // If item is provided (update scenario) use data from it.
	    // If not (create scenario), create an example object.
	    var temp : ItemProps["props"]
	    if (item == null) {
	        temp = {
		        id: 0,
		        url: "",
		        sleep_time: 60,
		        make_screenshots: true}
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
		                    <Form.Control type="url" defaultValue={temp.url} readOnly={props.editMode}/>
		                    <Form.Text className="text-muted">
		                    </Form.Text>
		                </Form.Group>
		                <Form.Group controlId="sleep_time">
		                    <Form.Label>How often (in minutes) should the page be checked</Form.Label>
		                    <Form.Control as="select">
                                <option>{Math.ceil(temp.sleep_time/60)}</option>
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
		                <Form.Group controlId="make_screenshots">
		                    <Form.Check type="checkbox" label="Make screenshots" defaultChecked={temp.make_screenshots}/>
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
