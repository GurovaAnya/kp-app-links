import React, {useEffect, useState} from "react";
import {useParams} from "react-router-dom"
import EditIcon from '@mui/icons-material/Edit';
import {Button, TextField} from "@material-ui/core";
import "./DocumentInfo.css"
import axios from "axios";

const DocumentInfo = () => {
    const {id} = useParams();

    const [document, setDocument] = useState({
        "document": {},
        "children": [],
        "parents": []
    });

    useEffect(() => {
    let mounted = true;
    fetch('/api/document/' + id).then(data => data.json()).then(doc => {
      if (mounted){
        setDocument(doc);
      }
    })
    return () => mounted = false;
  }, [])


    return (
        <div className="doc-container">
            <div className="doc-name">{document.document.name}</div>
            <div className="doc-relation-info-container">
                <div className="doc-relation-info-header">
                    Ссылается на другие законы:
                </div>
                {
                    document.children.map((child) => {
                        return <RelationInfo key={child.id} child={child}/>
                    })
                }
            </div>
            <div className="doc-relation-info-container">
                <div className="doc-relation-info-header">
                    Ссылающиеся законы:
                </div>
                {
                    document.parents.map((parent) => {
                         return <RelationInfo key={parent.id} child={parent}/>
                    })
                }
            </div>
        </div>
    )
}

export default DocumentInfo

const RelationInfo = (props) => {
    const text = props.child.text;

    return  (
        <>
            <div>
                {props.child.name} ({props.child.start_index}:{props.child.end_index})
            </div>
            {
                (
                    <>
                        <Highlighted
                            text={props.child.text}
                            start={props.child.start_index}
                            end={props.child.end_index}
                            id={props.child.link_id}
                        />
                    </>
                )
            }
        </>)
}

const Highlighted = ({ text = "", start, end, id}) => {

    const [startIdx, setStartIdx] = useState(start);
    const [endIdx, setEndIdx] = useState(end);
    const [isEditMode, setIsEditMode] = useState(false);


    const handleMouseUp = async () => {
        const selection = window.getSelection();
        const anchor = selection.anchorOffset;
        const focus = selection.focusOffset;
        const start_index = Math.min(anchor, focus);
        const end_index = Math.max(anchor, focus);
        console.log(`Selected text: ${window.getSelection().toString()}`);
        console.log(start_index, end_index);
        setStartIdx(start_index);
        setEndIdx(end_index);
    }

    const saveNewRelationIndexes = async () => {
        await axios.post('/api/save_new_relation_indexes/' + id,
            {"start_index": startIdx, "end_index": endIdx} );

    }

    const save = async () => {
        setIsEditMode(false);
        await saveNewRelationIndexes();
    }

    return (
        <>
            <div
                id={"law-text-" + id}
                onMouseUp={handleMouseUp}
            >
                {isEditMode && text}

                {!isEditMode &&
                    <>
                        {text.substring(0, startIdx)}
                        <u>{text.substring(startIdx, endIdx)}</u>
                        {text.substring(endIdx)}
                        <EditIcon fontSize="small" onClick={() => setIsEditMode(true)}/>
                    </>
                }


            </div>
            {isEditMode && (<Button onClick={() => save()}>Сохранить</Button>)}
        </>
    )
};