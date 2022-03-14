import React, {useEffect, useRef, useState} from 'react';
import cytoscape from 'cytoscape';
import "./styles.css";


export function Graph(){
  const cyto = useRef();

  const [graph, setGraph] = useState([]);

  useEffect(() => {
    let mounted = true;
    fetch('http://localhost:3000/test').then(data => data.json()).then(items => {
      if (mounted){
        console.log(items)
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
        }
      ],

      elements: graph
    });

  }, [graph]);

  return (
      <div className="app-body-section app-main-section flex-direction-column" ref={cyto} />
  );
}