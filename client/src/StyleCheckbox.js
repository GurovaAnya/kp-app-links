import {Checkbox, FormControlLabel} from "@mui/material";
import React from "react";

export const StyleCheckbox = ({styleId, show, setShow, restore, filter, label}) => {
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