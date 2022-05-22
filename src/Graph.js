import React, {useEffect, useRef, useState} from 'react';
import cytoscape from 'cytoscape';
import "./styles.css";
import {useNavigate} from "react-router-dom";
import {SideMenu} from "./SideMenu";


export function Graph() {
    const cyto = useRef();
    const navigate = useNavigate();
    const [graph, setGraph] = useState({"edges": [], "nodes": []});
    const [classesToHide, setClassesToHide] = useState({});

    const filter = (classes) => {
        const classesToHideCopy = classesToHide;
        classesToHideCopy[classes] = cy.$(classes).remove()
        setClassesToHide(classesToHideCopy);
    }
    const restore = (classes) => {
        const classesToHideCopy = classesToHide;
        const dataToRestore = classesToHideCopy[classes];
        cy.add(dataToRestore);
        delete classesToHideCopy[classes];
        setClassesToHide(classesToHideCopy);
    }

    useEffect(() => {
        let mounted = true;
        fetch('/api/nodes').then(data => data.json()).then(items => {
            if (mounted) {
                console.log(items);
                setGraph(items);
            }
        })
        return () => mounted = false;
    }, [])

    let cy;

    useEffect(() => {
        cy = cytoscape({
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
                        'line-color': "#9090fa"
                    }
                },
                {
                    selector: ".0",
                    style: {
                        "line-color": "#6fb656"
                    }
                },
                {
                    selector: ".1",
                    style: {
                        "line-color": "#e53b3b"
                    }
                },
                {
                    selector: ".2",
                    style: {
                        "line-color": "#4570d2"
                    }
                }
            ],

            elements: graph
        });

        cy.nodes().on('click', function (e) {
            const nodeData = e.target.data();
            navigate("document/" + nodeData.id);
        })

    }, [graph]);

    return (
        <>

            <SideMenu filter={filter} restore={restore}/>
            <div className="graph" ref={cyto}/>
        </>

    );
}
