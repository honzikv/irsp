import {
    AlertColor,
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    SvgIconTypeMap,
} from '@mui/material'
import { OverridableComponent } from '@mui/material/OverridableComponent'
import { Fragment, FunctionComponent, useState } from 'react'

export interface ConfirmationDialogProps {
    onConfirm: () => any
    onCancel?: () => any
    triggerButtonColor: AlertColor
    triggerButtonText: string
    triggerButtonVariant: 'text' | 'outlined' | 'contained'
    confirmButtonColor?: AlertColor
    cancelButtonColor?: AlertColor
    title: string
    message: string
    StartIcon?: OverridableComponent<SvgIconTypeMap>
}

const ButtonActionConfirmationDialog: FunctionComponent<
    ConfirmationDialogProps
> = ({
    onConfirm,
    onCancel,
    triggerButtonColor,
    triggerButtonText,
    triggerButtonVariant,
    confirmButtonColor,
    cancelButtonColor,
    message,
    title,
    StartIcon
}) => {
    const [open, setOpen] = useState(false)

    const onClose = () => {
        if (onCancel) {
            onCancel()
        }
        setOpen(false)
    }

    const onConfirmClick = () => {
        onConfirm()
        setOpen(false)
    }

    return (
        <Fragment>
            <Button
                variant={triggerButtonVariant}
                color={triggerButtonColor}
                onClick={() => setOpen(true)}
                startIcon={StartIcon ? <StartIcon /> : <></>}
            >
                {triggerButtonText}
            </Button>

            <Dialog open={open} onClose={onClose}>
                <DialogTitle>Confirm</DialogTitle>
                <DialogContent>
                    <DialogContentText>{message}</DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button
                        onClick={onClose}
                        color={cancelButtonColor || 'secondary'}
                        variant="contained"
                    >
                        Cancel
                    </Button>
                    <Button
                        onClick={onConfirmClick}
                        color={confirmButtonColor || 'primary'}
                        variant="contained"
                    >
                        Confirm
                    </Button>
                </DialogActions>
            </Dialog>
        </Fragment>
    )
}

export default ButtonActionConfirmationDialog
