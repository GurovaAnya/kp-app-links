import React, {useEffect, useRef, useState} from 'react';
import cytoscape from 'cytoscape';
import "./styles.css";
import {useNavigate} from "react-router-dom";
import {SideMenu} from "./SideMenu";


export function Graph({showSideMenu}) {
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

    const focusById = (id) => {
        if (id === null || id === undefined)
            cy.fit(cy.nodes, 100);
        else
            cy.fit(cy.$('#'+id), 300);
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
                    selector: 'edge.hover',
                    style: {
                        'label': 'data(type)'
                    }
                },
                {
                    selector: "node[name]",
                    style: {
                        content: "data(name)",
                        "text-wrap": "wrap",
                        "text-max-width": 300
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
                        "line-color": "#dac13f"
                    }
                },
                {
                    selector: ".2",
                    style: {
                        "line-color": "#4570d2"
                    }
                },
                {
                    selector: ".3",
                    style:{
                        "line-color": "#e53b3b"
                    }
                }
            ],

            elements: graph
        });

        cy.nodes().on('click', function (e) {
            const nodeData = e.target.data();
            navigate("document/" + nodeData.id);
        })

        cy.edges().on('mouseover', function (e){
            e.target.addClass('hover');
        })

        cy.edges().on('mouseout', function (e){
            e.target.removeClass('hover');
        })

    }, [graph]);

    console.log("Graph", showSideMenu);
    return (
        <div className={"graph-flex-container"}>
            {showSideMenu && (
                <div className={"side-menu"} >
                    <SideMenu
                        className={"graph-flex-child"}
                        filter={filter}
                        restore={restore}
                        names={graph.nodes}
                        focusByName={(id) => focusById(id)}/>
                </div>
            )}
            <div className={"graph-flex-child"}>
                <div className="graph" ref={cyto}/>
            </div>
        </div>

    );
}
