import React, {useEffect, useRef, useState} from 'react';
import cytoscape from 'cytoscape';
import "./styles.css";


export function Graph(){
  const cyto = useRef();

  const [graph, setGraph] = useState([]);

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
        }
      ],

      elements: graph
    });

  }, [graph]);

  return (
      <div className="graph" ref={cyto}/>
  );
}

// const getItems = () => {
//   return {
//     "nodes":[
//         {
//             'data':
//                 {
//                     "id": 1,
//                     'name': "Постановление Правительства российской федерации от 31 декабря 2021 г. № 2611"
//                 }
//         },
//         {
//             'data':
//                 {
//                     'id': 2,
//                     'name': 'Постановление Правительства РФ от 10 февраля 2021 г. N 147'
//                 }
//         },
//         {
//             'data':
//                 {
//                     'id': 3,
//                     'name': 'Постановление Правительства РФ от 10 марта 2020 г. N 263'
//                 }
//         },
//         {
//             'data':
//                 {
//                     'id': 4,
//                     'name': 'Статья 214 ГК РФ'
//                 }
//         },
//         {
//             'data':
//                 {
//                     'id': 5,
//                     'name': 'Статья 215 ГК РФ'
//                 }
//         },
//         {
//             'data':
//                 {
//                     'id': 6,
//                     'name': 'Статья 9 ТК РФ'
//                 }
//         },
//         {
//             'data':
//                 {
//                     'id': 7,
//                     'name': 'Статья 125 ГК РФ'
//                 }
//         }
//     ],
//     "edges":[
//         {
//             'data':
//                 {
//                     "source": 1,
//                     "target": 2
//                 }
//         },
//         {
//             'data':
//                 {
//                     "source": 2,
//                     "target": 3
//                 }
//         },
//         {
//             'data':
//                 {
//                     "source": 4,
//                     "target": 7
//                 }
//         }
//     ]
//   }
// }