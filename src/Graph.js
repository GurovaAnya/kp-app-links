import React, {useEffect, useRef, useState} from 'react';
import cytoscape from 'cytoscape';
import "./styles.css";
import {useNavigate} from "react-router-dom";
import Button from "@mui/material/Button";
import Input from "@mui/material/Input";
import {Checkbox, FormControlLabel} from "@mui/material";


export function Graph() {
    const cyto = useRef();
    const navigate = useNavigate();
    const [graph, setGraph] = useState({"edges": [], "nodes": []});
    const [classesToHide, setClassesToHide] = useState([]);

    const filter = (classes) => {
        setClassesToHide(classesToHide.concat(classes));
    }
    const restore = (classes) => {
        setClassesToHide(classesToHide.filter((v) => v !== classes));
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

        classesToHide.forEach((c) =>
            cy.$(c).remove()
        );

    }, [graph, classesToHide]);

    return (
        <>

            <SideMenu filter={filter} restore={restore}/>
            <div className="graph" ref={cyto}/>
        </>

    );
}

const SideMenu = ({filter, restore}) => {
    const [classes, setClasses] = useState(".-1");
    const [showImplicit, setShowImplicit] = useState(true);
    const [show0, setShow0] = useState(true);
    const [show1, setShow1] = useState(true);
    const [show2, setShow2] = useState(true);
    const [showNone, setShowNone] = useState(true);

    return <div>
        <Input
            value={classes}
            onChange={(val) => setClasses(val.target.value)}
        />
        <Button onClick={() => filter(classes)}>Remove</Button>
        <Button onClick={() => restore(classes)}>Restore</Button>
        <StyleCheckbox
            styleId={".implicit"}
            show={showImplicit}
            setShow={setShowImplicit}
            restore={restore}
            filter={filter}
            label={"Показывать неявные ссылки"}
        />
        <StyleCheckbox
            styleId=".0"
            show={show0}
            setShow={setShow0}
            restore={restore}
            filter={filter}
            label={"А принят в соотвествии с Б"}
        />
        <StyleCheckbox
            styleId=".1"
            show={show1}
            setShow={setShow1}
            restore={restore}
            filter={filter}
            label={"А регулируется Б"}
        />
        <StyleCheckbox
            styleId=".2"
            show={show2}
            setShow={setShow2}
            restore={restore}
            filter={filter}
            label={"А вносит изменения в Б"}
        />
        <StyleCheckbox
            styleId=".none"
            show={showNone}
            setShow={setShowNone}
            restore={restore}
            filter={filter}
            label={"Не задано"}
        />
    </div>
}

const StyleCheckbox = ({styleId, show, setShow, restore, filter, label}) => {
    return (
        <div>
            <FormControlLabel
                value={label}
                label={label}
                control={
                    <Checkbox
                        value={show}
                        checked={show}
                        onChange={(event, checked) => {
                            if (checked)
                                restore(styleId);
                            else
                                filter(styleId);
                            setShow(checked);
                        }
                        }

                    />}
            />
        </div>
    );
}