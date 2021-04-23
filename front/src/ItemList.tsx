import React from "react";

import {Card, ToggleButton, ToggleButtonGroup, ListGroup} from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

import Item from "./Item";
import ItemProps from "./Item";
import EditModal from "./EditModal";

type ItemListProps = {
    handleUpdate : any;
    handleDelete : any;
    items : Array<ItemProps["props"]>;
    visibleCount : number;
    refresh : any;
}

function ItemList (props : ItemListProps) {
    // It's used to describe which tab is currently chosen (only visibleCount of items is display simultaenously).
    const [tab, setTab] = React.useState(0);
    const [showEditModal, setShowEditModal] = React.useState(false);
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
	      { props.items.length !== 0 ?
            <div className="Items m-2">
	            <ListGroup>
	                {renderItems(props.items, props.visibleCount)}
	            </ListGroup>
	        </div> :
            <div>
              <Card bg="light" id="centered-form">
                  <Card.Body >
                      It's so empty here... <br/>
                      Add something to the watch list using the "Create" button
                  </Card.Body>
              </Card>

            </div>
          }
	      <div className="Controls m-2 mt-1">
	          <ToggleButtonGroup type="radio" onChange={(val : number) => setTab(val)} name="tab" defaultValue={0}>
	              {renderTabButtons(props.items.length, props.visibleCount)}
	          </ToggleButtonGroup>
	      </div>
	      <EditModal show={showEditModal} handleTask={(json : ItemProps["props"]) => props.handleUpdate(json)} onHide={() => {setShowEditModal(false);}} item={activeItem} editMode={true} handleDelete={(json: ItemProps["props"]) => props.handleDelete(json)} closeModal={() => setShowEditModal(false)} refresh={() => props.refresh()}/>
      </div>
  );
};

export default ItemList;
