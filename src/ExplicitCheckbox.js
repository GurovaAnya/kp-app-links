import {Checkbox, FormControlLabel} from "@mui/material";
import React from "react";

export const ExplicitCheckbox = ({
                                     show0,
                                     setShow0,
                                     show1,
                                     setShow1,
                                     show2,
                                     setShow2,
                                     show3,
                                     setShow3,
                                     showNone,
                                     setShowNone,
                                     children,
                                     filter,
                                     restore
                                 }) => {

    const handleParentChange = (event) => {
        const checked = event.target.checked;
        handleChangeAndShow(show0, setShow0, filter, restore, ".0", checked);
        handleChangeAndShow(show1, setShow1, filter, restore, ".1", checked);
        handleChangeAndShow(show2, setShow2, filter, restore, ".2", checked);
        handleChangeAndShow(show3, setShow3, filter, restore, ".3", checked);
        handleChangeAndShow(showNone, setShowNone, filter, restore, ".none", checked);

    }

    const handleChangeAndShow = (show, setShow, filter, restore, id, checked) => {
        if (show === checked)
            return;
        if (show)
            filter(id);
        else
            restore(id);
        setShow(checked);
    }

    return (
        <div>
            <FormControlLabel
                label="Показывать явные ссылки"
                control={
                    <Checkbox
                        checked={show0 && show1 && show2 && show3 && showNone}
                        indeterminate={!(show0 && show1 && show2 && show3 && showNone) && (show0 || show1 || show2 || show3 || showNone)}
                        onChange={handleParentChange}
                    />
                }
            />
            {children}
        </div>
    );
}