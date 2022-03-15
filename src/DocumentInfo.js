import React from "react";
import {useParams} from "react-router-dom"

const DocumentInfo = () => {
    let {id} = useParams();
    return (
        <div>document {id} info</div>
    )
}

export default DocumentInfo