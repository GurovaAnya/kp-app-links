import React, {useEffect, useRef, useState} from 'react';
import cytoscape from 'cytoscape';
import "./styles.css";
import { useNavigate } from "react-router-dom";


export function Graph(){
  const cyto = useRef();
  const navigate = useNavigate();
  const [graph, setGraph] = useState({"edges":[],"nodes":[]});

  useEffect(() => {
    let mounted = true;
    fetch('/api/nodes').then(data => data.json()).then(items => {
      if (mounted){
        setGraph(items);
      }
    })
    return () => mounted = false;
  }, [])

  useEffect(() => {
    let cy = cytoscape({
      container: cyto.current,

      style: [
        {
          selector: "node[name]",
          style: {
            content: "data(name)"
          }
        },

        {
          selector: "edge",
          style: {
            "curve-style": "bezier",
            "target-arrow-shape": "triangle"
          }
        },
        {
          selector: ".implicit",
          style: {
            'line-style': 'dashed',
            "target-arrow-shape": "none",
            'line-color': "#0000FF"
          }
        }
      ],

      elements: graph
    });

    cy.nodes().on('click', function(e) {
      const nodeData = e.target.data();
      navigate("document/" + nodeData.id);
    })
      }, [graph]);

  return (
      <div className="graph" ref={cyto}/>
  );
}