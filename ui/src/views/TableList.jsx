/*!

=========================================================
* Light Bootstrap Dashboard React - v1.3.0
=========================================================

* Product Page: https://www.creative-tim.com/product/light-bootstrap-dashboard-react
* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/light-bootstrap-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React, { Component } from "react";
import { Grid, Row, Col, Table } from "react-bootstrap";

import Card from "components/Card/Card.jsx";
import { thArray, tdArray } from "variables/Variables.jsx";
import axios from 'axios'



class TableList extends Component {



  constructor(props) {
    super(props);
    this.state = {
        stat_tags: [],
        stat_vals: []
        
  
    };
  }
  
  getStats() {
    axios
        .get(`http://127.0.0.1:5001/generalstats`, {})
        .then(res => {
            const data = res.data
            const generalstats = data

            var stat_tags = Object.keys(data).map(val => val);
            var stat_vals = Object.keys(data).map(val => data[val]);
            console.log(stat_vals);
                this.setState({
                    stat_tags:stat_tags,
                    stat_vals:stat_vals
                })
        })
        .catch((error) => {
            console.log(error)
        })
      }


componentDidMount(){
        this.getStats();
        console.log(this.state)
  }    
  render() {
    return (
      <div className="content">
        <Grid fluid>
          <Row>
            <Col md={12}>
              <Card
                title="General statistics data"
                category="descriptive statistics"
                ctTableFullWidth
                ctTableResponsive
                content={
                  <Table striped hover>
                    <thead>
                    <tr>
                        {this.state.stat_tags.slice(1,5).map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </thead>
                    <tbody>
                    <tr>
                        {this.state.stat_vals.slice(1,5).map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </tbody>
                  </Table>
                }
              />
            </Col>

         
            <Col md={12}>
              <Card
                title="General statistics data"
                category="descriptive statistics"
                ctTableFullWidth
                ctTableResponsive
                content={
                  <Table striped hover>
                    <thead>
                    <tr>
                        {this.state.stat_tags.slice(5,10).map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </thead>
                    <tbody>
                    <tr>
                        {this.state.stat_vals.slice(5,10).map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </tbody>
                  </Table>
                }
              />
            </Col>

            <Col md={12}>
              <Card
                title="General statistics data"
                category="descriptive statistics"
                ctTableFullWidth
                ctTableResponsive
                content={
                  <Table striped hover>
                    <thead>
                    <tr>
                        {this.state.stat_tags.slice(10,15).map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </thead>
                    <tbody>
                    <tr>
                        {this.state.stat_vals.slice(10,15).map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </tbody>
                  </Table>
                }
              />
            </Col>
            


            <Col md={12}>
              <Card
                title="General statistics data"
                category="descriptive statistics"
                ctTableFullWidth
                ctTableResponsive
                content={
                  <Table striped hover>
                    <thead>
                    <tr>
                        {this.state.stat_tags.slice(15,20).map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </thead>
                    <tbody>
                    <tr>
                        {this.state.stat_vals.slice(15,20).map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </tbody>
                  </Table>
                }
              />
            </Col>



            <Col md={12}>
              <Card
                title="General statistics data"
                category="descriptive statistics"
                ctTableFullWidth
                ctTableResponsive
                content={
                  <Table striped hover>
                    <thead>
                    <tr>
                        {this.state.stat_tags.slice(20,25).map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </thead>
                    <tbody>
                    <tr>
                        {this.state.stat_vals.slice(20,25).map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </tbody>
                  </Table>
                }
              />
            </Col>


            <Col md={12}>
              <Card
                title="General statistics data"
                category="descriptive statistics"
                ctTableFullWidth
                ctTableResponsive
                content={
                  <Table striped hover>
                    <thead>
                    <tr>
                        {this.state.stat_tags.slice(25,30).map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </thead>
                    <tbody>
                    <tr>
                        {this.state.stat_vals.slice(25,30).map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </tbody>
                  </Table>
                }
              />
            </Col>


            <Col md={12}>
              <Card
                title="General statistics data"
                category="descriptive statistics"
                ctTableFullWidth
                ctTableResponsive
                content={
                  <Table striped hover>
                    <thead>
                    <tr>
                        {this.state.stat_tags.slice(30,34).map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </thead>
                    <tbody>
                    <tr>
                        {this.state.stat_vals.slice(30,34).map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </tbody>
                  </Table>
                }
              />
            </Col>

          </Row>
        </Grid>
      </div>
    );
  }
}

export default TableList;
