import {
    AlertColor,
    Button,
    ButtonTypeMap,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    ExtendButtonBase,
} from '@mui/material'
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
                // startIcon={<TriggerButtonIcon /> ?? <></>}
                color={triggerButtonColor}
                onClick={() => setOpen(true)}
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
