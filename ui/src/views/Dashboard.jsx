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
import ChartistGraph from "react-chartist";
import { Grid, Row, Col } from "react-bootstrap";
import axios from 'axios'
import { Card } from "components/Card/Card.jsx";
import { StatsCard } from "components/StatsCard/StatsCard.jsx";
import { Tasks } from "components/Tasks/Tasks.jsx";
import {
  dataPie,
  legendPie,
  dataSales,
  optionsSales,
  responsiveSales,
  legendSales,
  dataBar,
  optionsBar,
  responsiveBar,
  legendBar
} from "variables/Variables.jsx";

class Dashboard extends Component {


  constructor(props) {
    super(props);
    this.state = {
        cities: [],
        sites: [],
        companies: [],
        count: "",
        numcompanies: "",

        piechart:{}
    };
  }

  createLegend(json) {
    var legend = [];
    for (var i = 0; i < json["names"].length; i++) {
      var type = "fa fa-circle text-" + json["types"][i];
      legend.push(<i className={type} key={i} />);
      legend.push(" ");
      legend.push(json["names"][i]);
    }
    return legend;
  }

  

  getCities() {
    axios

        .get(`http://127.0.0.1:5001/cities/`, {})
        .then(res => {
            const data = res.data
            const cities = data.map(u =>
                <div>
                <p>{u}</p>
                
                </div>
                )

                this.setState({
                    cities
                })

        })
        .catch((error) => {
            console.log(error)
        })
      }

  getSites() {
      axios

          .get(`http://127.0.0.1:5001/sites/`, {})
          .then(res => {
              const data = res.data
              const sites = data.map(u =>
                  <div>
                  <p>{u}</p>
                  
                  </div>
                  )

                  this.setState({
                      sites
                  })

          })
          .catch((error) => {
              console.log(error)
          })
  }

  getchart1() {
    axios

        .get(`http://127.0.0.1:5001/companieschart/`, {})
        .then(res => {
            const data = res.data
            var percentages = Object.keys(data).map(val => data[val]);
            var types = Object.keys(data).map(val =>"info");
            var percentages_string = Object.keys(data).map(val => data[val]+"%" );
            var tags = Object.keys(data).map(val => val);
            var lpdata = {names:tags,types:types}
            var legendPie = this.createLegend(lpdata);
            var pc = {
              dataPie:{
                labels:percentages_string,
                series: percentages
              },
              legendPie:legendPie
            };
            console.log(pc);
            this.setState({
              piechart:pc
          })

        })
        .catch((error) => {
            console.log(error)
        })
  }

  getCompanies() {
    axios

        .get(`http://127.0.0.1:5001/companies/`, {})
        .then(res => {
            const data = res.data
            const companies = data.slice(0,10).map(u =>
                <div>
                  <ul>
                    <li>{u}</li>
                  </ul>
                </div>
                )

                this.setState({
                    companies:companies,
                    numcompanies: data.length
                })

        })
        .catch((error) => {
            console.log(error)
        })
  }

  getCount() {
    axios

        .get(`http://127.0.0.1:5001/offers/count`, {})
        .then(res => {
            const data = res.data
            this.setState({ count:data})

        })
        .catch((error) => {
            console.log(error)
        })
  }

  componentDidMount(){
    this.getchart1()
    this.getCities()
    this.getCount()
    this.getSites()
    this.getCompanies()
  }
  
  render() {

    
    return (
      <div className="content">
        <Grid fluid>
          <Row>
            <Col lg={3} sm={6}>
              <StatsCard
                bigIcon={<i className="pe-7s-server text-warning" />}
                statsText="Data"
                statsValue= {this.state.count}
                statsIcon={<i className="fa fa-refresh" />}
                statsIconText="Total amount of offers"
              />
            </Col>
            <Col lg={3} sm={6}>
              <StatsCard
                bigIcon={<i className="pe-7s-wallet text-success" />}
                statsText="Cities"
                statsValue={this.state.cities}
                statsIcon={<i className="fa fa-calendar-o" />}
                statsIconText="Cities studied"
              />
            </Col>
            <Col lg={3} sm={6}>
              <StatsCard
                bigIcon={<i className="pe-7s-graph1 text-danger" />}
                statsText="Sites"
                statsValue={this.state.sites}
                statsIcon={<i className="fa fa-clock-o" />}
                statsIconText="Sites studied"
              />
            </Col>
            <Col lg={3} sm={6}>
              <StatsCard
                bigIcon={<i className="fa fa-twitter text-info" />}
                statsText="Companies"
                statsValue={this.state.numcompanies}
                statsIcon={<i className="fa fa-refresh" />}
                statsIconText="Companies detected"
              />
            </Col>
          </Row>
          <Row>
            <Col md={4}>
              <Card
                statsIcon="fa fa-history"
                id="chartHours"
                title="Users Behavior"
                category="24 Hours performance"
                stats="Updated 3 minutes ago"
                content={
                  <div className="ct-chart">
                    <ChartistGraph
                      data={dataSales}
                      type="Line"
                      options={optionsSales}
                      responsiveOptions={responsiveSales}
                    />
                  </div>
                }
                legend={
                  <div className="legend">{this.createLegend(legendSales)}</div>
                }
              />
            </Col>
            <Col md={8}>
              <Card
                statsIcon="fa fa-clock-o"
                title="Email Statistics"
                category="Last Campaign Performance"
                stats="Campaign sent 2 days ago"
                content={
                  <div
                    id="chartPreferences"
                    className="ct-chart ct-perfect-fourth"
                  >
                    <ChartistGraph data={this.state.piechart.dataPie} type="Pie" />
                  </div>
                }
                legend={
                  <div className="legend">{this.state.piechart.legendPie}</div>
                }
              />
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Card
                id="chartActivity"
                title="2014 Sales"
                category="All products including Taxes"
                stats="Data information certified"
                statsIcon="fa fa-check"
                content={
                  <div className="ct-chart">
                    <ChartistGraph
                      data={dataBar}
                      type="Bar"
                      options={optionsBar}
                      responsiveOptions={responsiveBar}
                    />
                  </div>
                }
                legend={
                  <div className="legend">{this.createLegend(legendBar)}</div>
                }
              />
            </Col>

            <Col md={6}>
              <Card
                title="Companies studied"
                category="list of companies"
                stats="last companies"
                statsIcon="fa fa-history"
                content=
                  {this.state.companies}
                
              />
            </Col>
          </Row>
        </Grid>
      </div>
    );
  }
}

export default Dashboard;
