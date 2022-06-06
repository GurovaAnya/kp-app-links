import {ExplicitCheckbox} from "./ExplicitCheckbox";
import {Box} from "@mui/material";
import {StyleCheckbox} from "./StyleCheckbox";
import React from "react";

export const AllCheckboxes = ({show0, show1, show2, show3, showNone, show, show4, show5, show6, showNone1, filter,restore}) => {
    return (
        <ExplicitCheckbox
            show0={show0}
            show1={show1}
            show2={show2}
            show3={show3}
            showNone={showNone}
            setShow0={show}
            setShow1={show4}
            setShow2={show5}
            setShow3={show6}
            setShowNone={showNone1}
            filter={filter}
            restore={restore}
            children={

                <Box sx={{display: "flex", flexDirection: "column", ml: 3}}>
                    <StyleCheckbox
                        styleId=".0"
                        show={show0}
                        setShow={show}
                        restore={restore}
                        filter={filter}
                        label={"А принят в соотвествии с Б"}
                    />
                    <StyleCheckbox
                        styleId=".1"
                        show={show1}
                        setShow={show4}
                        restore={restore}
                        filter={filter}
                        label={"А регулируется Б"}
                    />
                    <StyleCheckbox
                        styleId=".2"
                        show={show2}
                        setShow={show5}
                        restore={restore}
                        filter={filter}
                        label={"А вносит изменения в Б"}
                    />
                    <StyleCheckbox
                        styleId=".3"
                        show={show3}
                        setShow={show6}
                        restore={restore}
                        filter={filter}
                        label={"А признает утратившим силу Б"}
                    />
                    <StyleCheckbox
                        styleId=".none"
                        show={showNone}
                        setShow={showNone1}
                        restore={restore}
                        filter={filter}
                        label={"Не задано"}
                    />
                </Box>}
        />);
}