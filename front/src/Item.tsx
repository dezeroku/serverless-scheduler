import React from "react";

import "bootstrap/dist/css/bootstrap.min.css";

type ItemProps = {
    id : number;
    url : string;
    sleep_time : number;
    make_screenshots : boolean;
}

type ItemState = {
}

class Item extends React.Component<ItemProps, ItemState> {
    state : ItemState = {}

    render () {
        return (
            <div className="Item">
	            <a href={this.props.url}>{this.props.url}</a>|
                sleep time: {Math.ceil(this.props.sleep_time / 60)} minutes|
	            diff screenshots: {this.props.make_screenshots.toString()}
            </div>
        );
    }
};

export default Item;
