import React, { Component } from 'react'
import { Accordion, Icon } from 'semantic-ui-react'
import activeregion from '../activeregion.jpeg';
import rgb from '../RGB.jpeg'
import keyplan from '../keyplan.jpeg'
export default class AccordionExampleStyled extends Component {
  state = { activeIndexs: new Set()}

  handleClick = (e, titleProps) => {

    const { index } = titleProps;
    const { activeIndex } = this.state;
    if(this.state.activeIndexs.has(index))  
        this.state.activeIndexs.delete(index);
    else
        this.state.activeIndexs.add(index);

    this.setState({activeIndexs: this.state.activeIndexs});
  }

    componentDidMount(){
        document.body.style = 'background: royalblue';
    }
  render() {
    const { activeIndexs } = this.state

    return (
      <Accordion styled>
        <Accordion.Title
          active={activeIndexs.has(0)}
          index={0}
          onClick={this.handleClick}
        >
          <Icon name='dropdown' />
          Active Region
        </Accordion.Title>
        <Accordion.Content active={activeIndexs.has(0)}>
          <img src={activeregion} width = {'100%'} height = {'250px'}></img>
        </Accordion.Content>

        <Accordion.Title
          active={activeIndexs.has(1)}
          index={1}
          onClick={this.handleClick}
        >
          <Icon name='dropdown' />
          RGB Images
        </Accordion.Title>
        <Accordion.Content active={activeIndexs.has(1)}>
        <img src={rgb} width = {'100%'} height = {'250px'}></img>
        </Accordion.Content>

        <Accordion.Title
          active={activeIndexs.has(2)}
          index={2}
          onClick={this.handleClick}
        >
          <Icon name='dropdown' />
          Segmentation Images
        </Accordion.Title>
        <Accordion.Content active={activeIndexs.has(2)}>
       
        </Accordion.Content>
        <Accordion.Title
          active={activeIndexs.has(3)}
          index={3}
          onClick={this.handleClick}
        >
          <Icon name='dropdown' />
            Thermal Images
        </Accordion.Title>
        <Accordion.Content active={activeIndexs.has(3)}>
       
        </Accordion.Content>
        <Accordion.Title
          active={activeIndexs.has(4)}
          index={4}
        >
            <h3>keyplan</h3>
        </Accordion.Title>
        <img src={keyplan} width = {'100%'} height = {'250px'}></img>
        
      </Accordion>
    )
  }
}