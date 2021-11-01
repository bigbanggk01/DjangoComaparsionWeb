import React, { Component } from "react";
import { render } from "react-dom";
class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
          data: [],
          loaded: false,
          placeholder: "Loading"
        };
    }

    componentDidMount() {
        fetch("api/product")
        .then(response => {
            if (response.status > 400) {
            return this.setState(() => {
                return { placeholder: "Something went wrong!" };
            });
            }
            return response.json();
        })
        .then(data => {
            this.setState(() => {
            return {
                data,
                loaded: true
            };
            });
            console.log(data);
        });
    }
    render() {return(
        this.state.data.map(product => {
            return (
                <div id="product-item" key={product.id} className="col">
                    <a className="card" href={product.url}>
                        <div id="product-image">
                            <img src={product.image_link} alt="rover" />
                        </div>
                        <div id="product-provider" className="badge bg-info text-center">
                            Tiki.vn
                        </div>
                        <div className="card-body">
                            <div className="tag tag-teal">{product.name}</div>
                            <div id="product-price">
                                {product.price}
                            </div>
                            <a id="product-button" href={product.url} class="button"><span>Mua ngay</span></a>
                        </div>
                    </a>
                </div>
            );
        })
    )}
}

export default App;

const container = document.getElementById("products");
render(<App />, container);